import asyncio
import time
from typing import Any, List, Tuple
from src.model_serving.engine.predictor import Predictor

class DynamicBatcher:
    def __init__(self, predictor: Predictor, max_batch_size: int = 32, timeout_ms: int = 10):
        self.predictor = predictor
        self.max_batch_size = max_batch_size
        self.timeout_secs = timeout_ms / 1000.0
        self.queue = asyncio.Queue()
        self.worker_task = asyncio.create_task(self._process_queue())

    async def _process_queue(self):
        while True:
            batch: List[Tuple[Any, asyncio.Future]] = []
            
            try:
                # Wait for at least one item
                item = await self.queue.get()
                batch.append(item)
                
                # Gather more items up to max_batch_size or timeout
                end_time = time.time() + self.timeout_secs
                while len(batch) < self.max_batch_size:
                    remaining_time = end_time - time.time()
                    if remaining_time <= 0:
                        break
                        
                    try:
                        item = await asyncio.wait_for(self.queue.get(), timeout=remaining_time)
                        batch.append(item)
                    except asyncio.TimeoutError:
                        break
                
                # Process batch
                inputs = [b[0] for b in batch]
                futures = [b[1] for b in batch]
                
                try:
                    # Run CPU-bound prediction in executor
                    loop = asyncio.get_event_loop()
                    predictions = await loop.run_in_executor(None, self.predictor.predict, inputs)
                    
                    for fut, pred in zip(futures, predictions):
                        if not fut.done():
                            fut.set_result(pred)
                except Exception as e:
                    for fut in futures:
                        if not fut.done():
                            fut.set_exception(e)
                            
            except Exception as e:
                # Handle general queue errors
                print(f"Batcher error: {e}")

    async def predict_async(self, input_data: Any) -> Any:
        future = asyncio.Future()
        await self.queue.put((input_data, future))
        return await future

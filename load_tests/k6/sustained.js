import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 50 },  // Ramp up
    { duration: '2m', target: 50 },   // Sustained
    { duration: '30s', target: 0 },   // Ramp down
  ],
};

export default function () {
  const url = 'http://localhost:8000/predict';
  const payload = JSON.stringify({
    model_name: 'default_model',
    inputs: [[Math.random(), Math.random(), Math.random(), Math.random()]]
  });

  const params = {
    headers: {
      'Content-Type': 'application/json',
      'X-API-Key': 'dev-key-123'
    },
  };

  const res = http.post(url, payload, params);
  
  check(res, {
    'is status 200': (r) => r.status === 200,
    'latency < 100ms': (r) => r.timings.duration < 100,
  });

  sleep(0.1);
}

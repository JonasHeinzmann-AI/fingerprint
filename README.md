# Canvas Fingerprint API

Welcome to the Canvas Fingerprint API! This API allows you to generate canvas fingerprints for browser instances, aiding in browser identification.

## Base URL
The base URL for the API is: `https://fingerprint-morcmqqs.b4a.run/`

## Generate Canvas Fingerprint Endpoint

### Endpoint
`POST /canvas-fingerprint`

### Description
This endpoint generates a canvas fingerprint based on various parameters, providing a unique identifier for the current browser instance.

### Request
- **Method:** POST
- **Headers:**
  - `Content-Type: application/json`
- **Body:**
  - Provide a JSON object with the following parameters:
    - `user_agent`: The user agent string of the browser.
    - `screen_resolution`: An array representing the screen resolution, e.g., `[1920, 1080]`.

### Example Request
```bash
curl -X POST -H "Content-Type: application/json" -d '{"user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",  "screen_resolution": [1920, 1080]}' https://fingerprint-morcmqqs.b4a.run/canvas-fingerprint
```

### Response
The response will be a JSON object containing the canvas fingerprint details.

### Example Response
```json
{
  "canvas_fingerprint":"8e5fea77",
  "screen_resolution":[1510,886],
  "user_agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
  "webgl_data":"eyJ2ZW5kb3IiOiAiVmVuZG9yIEIiLCAicmVuZGVyZXIiOiAiUmVuZGVyZXIgWSIsICJ2ZXJzaW9uIjogIlZlcnNpb24gMSIsICJleHRlbnNpb25zIjogW119"}
```

## Generate Canvas Image Endpoint (Under Construction)

### Endpoint
`POST /canvas-image`

### Note
This endpoint is currently under construction and may not provide accurate results. Please use the `/canvas-fingerprint` endpoint for reliable canvas fingerprint generation.

Feel free to check back later for updates on the status of the `/canvas-image` endpoint.

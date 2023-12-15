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
    - `webgl_data`: A JSON object containing WebGL data.
    - `screen_resolution`: An array representing the screen resolution, e.g., `[1920, 1080]`.

### Example Request
```bash
curl -X POST -H "Content-Type: application/json" -d '{"user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36", "webgl_data": {"vendor": "Vendor A", "renderer": "Renderer X", "version": "Version 1", "extensions": ["ext1", "ext2"]}, "screen_resolution": [1920, 1080]}' https://fingerprint-morcmqqs.b4a.run/canvas-fingerprint
```

### Response
The response will be a JSON object containing the canvas fingerprint details.

### Example Response
```json
{
  "canvas_fingerprint": "abc123xyz456",
  "timestamp": "2023-12-15T12:00:00Z"
}
```

## Generate Canvas Image Endpoint (Under Construction)

### Endpoint
`POST /canvas-image`

### Note
This endpoint is currently under construction and may not provide accurate results. Please use the `/canvas-fingerprint` endpoint for reliable canvas fingerprint generation.

Feel free to check back later for updates on the status of the `/canvas-image` endpoint.

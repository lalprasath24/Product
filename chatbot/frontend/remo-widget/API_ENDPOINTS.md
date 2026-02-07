# Backend API Endpoints Required

## File Management
- `POST /api/upload` - Upload .txt file to local folder
- `GET /api/files` - Get list of uploaded files
- `DELETE /api/files/:filename` - Delete specific file

## Chat
- `POST /api/chat` - Send message and get AI response

## Expected Responses

### Upload File
```json
{ "success": true, "filename": "document.txt" }
```

### Get Files
```json
[
  { "name": "document1.txt", "uploadDate": "2024-01-15" },
  { "name": "document2.txt", "uploadDate": "2024-01-16" }
]
```

### Chat
```json
{ "response": "AI generated response based on uploaded documents" }
```

## File Storage
Files should be stored in: `./uploads/` folder
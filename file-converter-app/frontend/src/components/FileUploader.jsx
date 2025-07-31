import React, { useCallback } from 'react'
import { Upload, X, File } from 'lucide-react'

const FileUploader = ({ files, onFilesChange, onFileRemove }) => {
  const onDrop = useCallback((e) => {
    e.preventDefault()
    const droppedFiles = Array.from(e.dataTransfer.files)
    onFilesChange(prev => [...prev, ...droppedFiles])
  }, [onFilesChange])

  const onDragOver = useCallback((e) => {
    e.preventDefault()
  }, [])

  const handleFileSelect = (e) => {
    const selectedFiles = Array.from(e.target.files)
    onFilesChange(prev => [...prev, ...selectedFiles])
  }

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
  }

  const getFileIcon = (fileName) => {
    const extension = fileName.split('.').pop()?.toLowerCase()
    const imageExtensions = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp', 'svg']
    const docExtensions = ['pdf', 'doc', 'docx', 'txt', 'rtf']
    
    if (imageExtensions.includes(extension)) {
      return '🖼️'
    } else if (docExtensions.includes(extension)) {
      return '📄'
    }
    return '📁'
  }

  return (
    <div className="space-y-4">
      {/* 드래그 앤 드롭 영역 */}
      <div
        onDrop={onDrop}
        onDragOver={onDragOver}
        className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-primary-400 transition-colors cursor-pointer"
        onClick={() => document.getElementById('file-input').click()}
      >
        <Upload className="w-8 h-8 mx-auto mb-4 text-gray-400" />
        <p className="text-gray-600 mb-2">
          파일을 여기에 드래그하거나 클릭하여 선택하세요
        </p>
        <p className="text-sm text-gray-500">
          최대 50MB까지 업로드 가능
        </p>
        <input
          id="file-input"
          type="file"
          multiple
          onChange={handleFileSelect}
          className="hidden"
          accept="image/*,.pdf,.doc,.docx,.txt,.rtf"
        />
      </div>

      {/* 업로드된 파일 목록 */}
      {files.length > 0 && (
        <div className="space-y-2">
          <h3 className="font-medium text-gray-700">업로드된 파일 ({files.length})</h3>
          <div className="max-h-48 overflow-y-auto space-y-2">
            {files.map((file, index) => (
              <div
                key={index}
                className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
              >
                <div className="flex items-center space-x-3">
                  <span className="text-lg">{getFileIcon(file.name)}</span>
                  <div className="min-w-0 flex-1">
                    <p className="text-sm font-medium text-gray-900 truncate">
                      {file.name}
                    </p>
                    <p className="text-xs text-gray-500">
                      {formatFileSize(file.size)}
                    </p>
                  </div>
                </div>
                <button
                  onClick={() => onFileRemove(index)}
                  className="p-1 hover:bg-gray-200 rounded-full transition-colors"
                >
                  <X className="w-4 h-4 text-gray-500" />
                </button>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default FileUploader 
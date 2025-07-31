import React from 'react'
import { Download, CheckCircle } from 'lucide-react'

const DownloadButton = ({ downloadUrl, fileName }) => {
  const handleDownload = () => {
    const link = document.createElement('a')
    link.href = downloadUrl
    link.download = fileName
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  }

  return (
    <div className="space-y-4">
      <div className="bg-green-50 border border-green-200 rounded-lg p-4">
        <div className="flex items-center">
          <CheckCircle className="w-5 h-5 text-green-600 mr-2" />
          <p className="text-green-800 font-medium">변환이 완료되었습니다!</p>
        </div>
      </div>
      
      <button
        onClick={handleDownload}
        className="w-full btn-primary flex items-center justify-center space-x-2"
      >
        <Download className="w-5 h-5" />
        <span>파일 다운로드</span>
      </button>
      
      <div className="text-center">
        <p className="text-sm text-gray-600">
          파일명: <span className="font-medium">{fileName}</span>
        </p>
        <p className="text-xs text-gray-500 mt-1">
          다운로드가 시작되지 않으면 버튼을 다시 클릭해주세요.
        </p>
      </div>
    </div>
  )
}

export default DownloadButton 
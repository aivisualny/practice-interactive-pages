import React, { useState, useEffect } from 'react'
import FileUploader from '../components/FileUploader'
import ConvertOptions from '../components/ConvertOptions'
import DownloadButton from '../components/DownloadButton'
import { FileText, Image, Download, Settings } from 'lucide-react'

const Home = () => {
  const [files, setFiles] = useState([])
  const [targetFormat, setTargetFormat] = useState('')
  const [compressionQuality, setCompressionQuality] = useState(85)
  const [isConverting, setIsConverting] = useState(false)
  const [downloadUrl, setDownloadUrl] = useState(null)
  const [error, setError] = useState(null)
  const [supportedFormats, setSupportedFormats] = useState(null)

  useEffect(() => {
    fetchSupportedFormats()
  }, [])

  const fetchSupportedFormats = async () => {
    try {
      const response = await fetch('/api/v1/formats')
      const data = await response.json()
      setSupportedFormats(data)
    } catch (error) {
      console.error('지원 형식 로드 실패:', error)
    }
  }

  const handleConvert = async () => {
    if (!files.length || !targetFormat) {
      setError('파일과 변환 형식을 선택해주세요.')
      return
    }

    setIsConverting(true)
    setError(null)
    setDownloadUrl(null)

    try {
      const formData = new FormData()
      files.forEach(file => {
        formData.append('files', file)
      })
      formData.append('target_format', targetFormat)
      formData.append('compression_quality', compressionQuality)

      const response = await fetch('/api/v1/convert', {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || '변환 중 오류가 발생했습니다.')
      }

      const blob = await response.blob()
      const url = URL.createObjectURL(blob)
      setDownloadUrl(url)
    } catch (error) {
      setError(error.message)
    } finally {
      setIsConverting(false)
    }
  }

  const handleFileRemove = (index) => {
    setFiles(files.filter((_, i) => i !== index))
  }

  const clearAll = () => {
    setFiles([])
    setTargetFormat('')
    setCompressionQuality(85)
    setDownloadUrl(null)
    setError(null)
  }

  return (
    <div className="container mx-auto px-4 py-8 max-w-4xl">
      {/* 헤더 */}
      <div className="text-center mb-8">
        <div className="flex items-center justify-center mb-4">
          <div className="bg-primary-600 p-3 rounded-full mr-4">
            <FileText className="w-8 h-8 text-white" />
          </div>
          <h1 className="text-4xl font-bold text-gray-900">FileForge</h1>
        </div>
        <p className="text-lg text-gray-600">
          간편하고 빠른 파일 변환 도구
        </p>
      </div>

      {/* 메인 컨텐츠 */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* 왼쪽 패널 - 파일 업로드 및 설정 */}
        <div className="space-y-6">
          <div className="card">
            <div className="flex items-center mb-4">
              <Image className="w-5 h-5 mr-2 text-primary-600" />
              <h2 className="text-xl font-semibold">파일 업로드</h2>
            </div>
            <FileUploader 
              files={files} 
              onFilesChange={setFiles}
              onFileRemove={handleFileRemove}
            />
          </div>

          <div className="card">
            <div className="flex items-center mb-4">
              <Settings className="w-5 h-5 mr-2 text-primary-600" />
              <h2 className="text-xl font-semibold">변환 설정</h2>
            </div>
            <ConvertOptions
              targetFormat={targetFormat}
              onTargetFormatChange={setTargetFormat}
              compressionQuality={compressionQuality}
              onCompressionQualityChange={setCompressionQuality}
              supportedFormats={supportedFormats}
            />
          </div>

          <div className="flex space-x-4">
            <button
              onClick={handleConvert}
              disabled={isConverting || !files.length || !targetFormat}
              className="btn-primary flex-1 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isConverting ? '변환 중...' : '변환 시작'}
            </button>
            <button
              onClick={clearAll}
              className="btn-secondary"
            >
              초기화
            </button>
          </div>
        </div>

        {/* 오른쪽 패널 - 결과 및 다운로드 */}
        <div className="card">
          <div className="flex items-center mb-4">
            <Download className="w-5 h-5 mr-2 text-primary-600" />
            <h2 className="text-xl font-semibold">변환 결과</h2>
          </div>
          
          {error && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-4">
              <p className="text-red-800">{error}</p>
            </div>
          )}

          {isConverting && (
            <div className="text-center py-8">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto mb-4"></div>
              <p className="text-gray-600">파일을 변환하고 있습니다...</p>
            </div>
          )}

          {downloadUrl && (
            <DownloadButton 
              downloadUrl={downloadUrl} 
              fileName={`converted_files.${targetFormat === 'zip' ? 'zip' : targetFormat}`}
            />
          )}

          {!isConverting && !downloadUrl && !error && (
            <div className="text-center py-8 text-gray-500">
              <FileText className="w-12 h-12 mx-auto mb-4 opacity-50" />
              <p>파일을 업로드하고 변환 형식을 선택한 후</p>
              <p>"변환 시작" 버튼을 클릭하세요.</p>
            </div>
          )}
        </div>
      </div>

      {/* 지원 형식 정보 */}
      {supportedFormats && (
        <div className="mt-8 card">
          <h3 className="text-lg font-semibold mb-4">지원되는 파일 형식</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h4 className="font-medium text-gray-700 mb-2">이미지 파일</h4>
              <p className="text-sm text-gray-600">
                {supportedFormats.image?.from?.join(', ').toUpperCase()}
              </p>
            </div>
            <div>
              <h4 className="font-medium text-gray-700 mb-2">문서 파일</h4>
              <p className="text-sm text-gray-600">
                {supportedFormats.document?.from?.join(', ').toUpperCase()}
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default Home 
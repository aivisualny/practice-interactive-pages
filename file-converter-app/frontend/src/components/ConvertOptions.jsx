import React from 'react'

const ConvertOptions = ({ 
  targetFormat, 
  onTargetFormatChange, 
  compressionQuality, 
  onCompressionQualityChange,
  supportedFormats 
}) => {
  const getAvailableFormats = () => {
    if (!supportedFormats) return []
    
    const formats = []
    if (supportedFormats.image) {
      formats.push(...supportedFormats.image.to.map(format => ({
        value: format,
        label: format.toUpperCase(),
        category: '이미지'
      })))
    }
    if (supportedFormats.document) {
      formats.push(...supportedFormats.document.to.map(format => ({
        value: format,
        label: format.toUpperCase(),
        category: '문서'
      })))
    }
    return formats
  }

  const isImageFormat = (format) => {
    const imageFormats = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'webp']
    return imageFormats.includes(format.toLowerCase())
  }

  return (
    <div className="space-y-4">
      {/* 변환 형식 선택 */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          변환할 형식
        </label>
        <select
          value={targetFormat}
          onChange={(e) => onTargetFormatChange(e.target.value)}
          className="input-field"
        >
          <option value="">형식을 선택하세요</option>
          {getAvailableFormats().map((format) => (
            <option key={format.value} value={format.value}>
              {format.label} ({format.category})
            </option>
          ))}
        </select>
      </div>

      {/* 압축 품질 설정 (이미지 형식인 경우에만 표시) */}
      {targetFormat && isImageFormat(targetFormat) && (
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            압축 품질: {compressionQuality}%
          </label>
          <input
            type="range"
            min="1"
            max="100"
            value={compressionQuality}
            onChange={(e) => onCompressionQualityChange(parseInt(e.target.value))}
            className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer slider"
          />
          <div className="flex justify-between text-xs text-gray-500 mt-1">
            <span>낮은 품질 (작은 파일)</span>
            <span>높은 품질 (큰 파일)</span>
          </div>
        </div>
      )}

      {/* 선택된 옵션 미리보기 */}
      {targetFormat && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <h4 className="font-medium text-blue-900 mb-2">변환 설정</h4>
          <div className="space-y-1 text-sm text-blue-800">
            <p>• 출력 형식: <span className="font-medium">{targetFormat.toUpperCase()}</span></p>
            {isImageFormat(targetFormat) && (
              <p>• 압축 품질: <span className="font-medium">{compressionQuality}%</span></p>
            )}
          </div>
        </div>
      )}
    </div>
  )
}

export default ConvertOptions 
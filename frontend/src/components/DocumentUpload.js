import React, { useState } from 'react';
import { Upload, Loader2 } from 'lucide-react';
import { api } from '../services/api';
export const DocumentUpload = ({ onUploadComplete }) => {
    const [uploading, setUploading] = useState(false);
    const [dragActive, setDragActive] = useState(false);
    const handleFile = async (file) => {
        setUploading(true);
        try {
            const result = await api.uploadDocument(file);
            console.log('Upload successful:', result);
            onUploadComplete();
            alert(`Successfully uploaded ${file.name}!\n${result.message}`);
        }
        catch (error) {
            console.error('Upload error:', error);
            alert(`Error uploading file: ${error.response?.data?.detail || error.message}`);
        }
        finally {
            setUploading(false);
        }
    };
    const handleDrag = (e) => {
        e.preventDefault();
        e.stopPropagation();
        if (e.type === 'dragenter' || e.type === 'dragover') {
            setDragActive(true);
        }
        else if (e.type === 'dragleave') {
            setDragActive(false);
        }
    };
    const handleDrop = (e) => {
        e.preventDefault();
        e.stopPropagation();
        setDragActive(false);
        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            handleFile(e.dataTransfer.files[0]);
        }
    };
    const handleChange = (e) => {
        if (e.target.files && e.target.files[0]) {
            handleFile(e.target.files[0]);
        }
    };
    return (<div className="p-4 border-b border-gray-200">
      <div className={`border-2 border-dashed rounded-lg p-6 text-center cursor-pointer transition-colors ${dragActive
            ? 'border-blue-500 bg-blue-50'
            : 'border-gray-300 hover:border-gray-400'} ${uploading ? 'opacity-50 cursor-not-allowed' : ''}`} onDragEnter={handleDrag} onDragLeave={handleDrag} onDragOver={handleDrag} onDrop={handleDrop} onClick={() => !uploading && document.getElementById('file-input')?.click()}>
        <input id="file-input" type="file" className="hidden" onChange={handleChange} accept=".pdf,.docx,.doc,.txt,.md" disabled={uploading}/>
        {uploading ? (<div className="flex flex-col items-center gap-2">
            <Loader2 className="w-8 h-8 text-blue-500 animate-spin"/>
            <p className="text-sm text-gray-600">Uploading and processing...</p>
          </div>) : (<div className="flex flex-col items-center gap-2">
            <Upload className="w-8 h-8 text-gray-400"/>
            <p className="text-sm text-gray-600">
              Drop a file here or click to upload
            </p>
            <p className="text-xs text-gray-500">
              Supported: PDF, DOCX, TXT, MD
            </p>
          </div>)}
      </div>
    </div>);
};

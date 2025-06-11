import React, { useState } from 'react';
import FileUpload from './components/FileUpload';
import StampControls from './components/StampControls';

function App() {
  const [pdfFile, setPdfFile] = useState<File | null>(null);
  const [stampFile, setStampFile] = useState<File | null>(null);

  return (
    <div className="p-4">
      <h1 className="text-xl font-bold mb-4">PDF Stamper</h1>
      <FileUpload
        onPdfSelect={setPdfFile}
        onStampSelect={setStampFile}
      />
      {pdfFile && stampFile && (
        <StampControls
          pdfFile={pdfFile}
          stampFile={stampFile}
        />
      )}
    </div>
  );
}

export default App;

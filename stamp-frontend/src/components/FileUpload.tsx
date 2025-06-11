type Props = {
    onPdfSelect: (file: File | null) => void;
    onStampSelect: (file: File | null) => void;
  };
  
  /**
   * FileUpload component allows users to upload a PDF and a stamp image.
   * @param {function} onPdfSelect - Callback function to handle PDF file selection.
   * @param {function} onStampSelect - Callback function to handle stamp image selection.
   */


const FileUpload = ({
    onPdfSelect,
    onStampSelect
}: Props)  => {
    return (
      <div className="flex flex-col gap-4">
        <div>
          <label className="block">Upload PDF:</label>
          <input type="file" accept="application/pdf" onChange={(e) => onPdfSelect(e.target.files ? e.target.files[0] : null)} />
        </div>
        <div>
          <label className="block">Upload Stamp Image (PNG):</label>
          <input type="file" accept="image/png" onChange={(e) => onStampSelect(e.target.files ? e.target.files[0] : null)} />
        </div>
      </div>
    );
  }

  export default FileUpload;
  
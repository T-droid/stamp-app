import React, { useEffect, useRef, useState } from "react";
import axios from "axios";
import { pdfjs } from "react-pdf";

pdfjs.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.min.js`;

type Props = {
  pdfFile: File;
  stampFile: File;
};
const StampControls = ({
    pdfFile,
    stampFile
} : Props) => {
//   const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const pdfCanvasRef = useRef<HTMLCanvasElement | null>(null);
  const stampCanvasRef = useRef<HTMLCanvasElement | null>(null);
  const [pdfDoc, setPdfDoc] = useState<pdfjs.PDFDocumentProxy | null>(null);
  const [stampImg, setStampImg] = useState<HTMLImageElement | null>(null);
  const [position, setPosition] = useState({ x: 100, y: 100 });
  const [isDragging, setIsDragging] = useState(false);
  const [scale, setScale] = useState(0.5);

  // Load PDF
  useEffect(() => {
    const loadPDF = async () => {
      const fileReader = new FileReader();
      fileReader.onload = async () => {
        if (fileReader.result) {
          const typedarray = new Uint8Array(fileReader.result as ArrayBuffer);
          const loadedPdf = await pdfjs.getDocument(typedarray).promise;
          setPdfDoc(loadedPdf);
        }
      };
      fileReader.readAsArrayBuffer(pdfFile);
    };
    loadPDF();
  }, [pdfFile]);

  // Load stamp image
  useEffect(() => {
    const reader = new FileReader();
    reader.onload = () => {
      const img = new Image();
      img.onload = () => setStampImg(img);
      if (typeof reader.result === "string") {
        img.src = reader.result;
      }
    };
    reader.readAsDataURL(stampFile);
  }, [stampFile]);

  // Render PDF once
  useEffect(() => {
    const renderPDF = async () => {
      if (!pdfDoc || !pdfCanvasRef.current) return;
      const page = await pdfDoc.getPage(1);
      const scaleFactor = 1.5;
      const viewport = page.getViewport({ scale: scaleFactor });
      const canvas = pdfCanvasRef.current;
      const ctx = canvas.getContext("2d");
      if (!ctx) {
        console.error("Failed to get 2D context");
        return;
      }

      canvas.width = viewport.width;
      canvas.height = viewport.height;

      await page.render({ canvasContext: ctx, viewport }).promise;

      // Set stamp canvas to same size
      if (stampCanvasRef.current) {
        stampCanvasRef.current.width = canvas.width;
        stampCanvasRef.current.height = canvas.height;
      }

      drawStamp(); // Initial draw
    };

    renderPDF();
  }, [pdfDoc, stampImg]);

  // Draw stamp on transparent layer
  const drawStamp = () => {
    if (!stampCanvasRef.current) return;
    const ctx = stampCanvasRef.current.getContext("2d");
    if (!ctx) return;
    ctx.clearRect(0, 0, stampCanvasRef.current.width, stampCanvasRef.current.height);
    if (stampImg) {
      const w = stampImg.width * scale;
      const h = stampImg.height * scale;
      ctx.drawImage(stampImg, position.x, position.y, w, h);
    }
  };

const handleMouseDown = (): void => {
    setIsDragging(true);
};


const handleMouseMove = (e: React.MouseEvent<HTMLCanvasElement>): void => {
    if (!isDragging) return;
    if (!stampCanvasRef.current) return;
    const rect = stampCanvasRef.current.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    setPosition({ x, y });
    drawStamp();
};

  const handleMouseUp = () => {
    setIsDragging(false);
  };

  const handleStampSubmit = async () => {
    const formData = new FormData();
    formData.append("pdf_file", pdfFile);
    formData.append("stamp_file", stampFile);
    formData.append("x", Math.round(position.x).toString());
    formData.append("y", Math.round(position.y).toString());
    formData.append("scale", scale.toString());
    formData.append("page_num", '0');

    try {
      const res = await axios.post("http://localhost:8000/stamp-pdf/", formData, {
        responseType: "blob",
      });

      const blob = new Blob([res.data], { type: "application/pdf" });
      const link = document.createElement("a");
      link.href = window.URL.createObjectURL(blob);
      link.download = "stamped_output.pdf";
      link.click();
    } catch (err) {
      alert("Failed to stamp PDF." + err);
    }
  };

  return (
    <div className="mt-4 relative inline-block">
      <canvas ref={pdfCanvasRef} />
      <canvas
        ref={stampCanvasRef}
        style={{ position: "absolute", top: 0, left: 0, cursor: "move" }}
        onMouseDown={handleMouseDown}
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUp}
      />
      <div className="mt-4 flex items-center gap-4">
        <label>Scale:</label>
        <input
          type="range"
          min="0.1"
          max="2"
          step="0.1"
          value={scale}
          onChange={(e) => {
            setScale(parseFloat(e.target.value));
            drawStamp();
          }}
        />
        <span>{scale}</span>
        <button
          onClick={handleStampSubmit}
          className="bg-blue-600 text-white px-4 py-2 rounded"
        >
          Stamp PDF
        </button>
      </div>
    </div>
  );
}

export default StampControls;

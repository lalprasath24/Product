import React, { useState } from "react";
import "./Header.css";
import ExcelReportModal from "./ExcelReportModal";

const Header = () => {
  const [isExcelModalOpen, setIsExcelModalOpen] = useState(false);

  return (
    <>
      <header className="header">
        <h1 className="logo">🥛 #############</h1>
        <div className="header-right">
          <nav className="nav">
            <a href="#">Home</a>
            <a href="/customers">customers</a>
            <a href="/products">Products</a>
            <a href="/plans">Plans</a>
            <a href="#">Orders</a>
            <a href="#">Profile</a>
          </nav>
          <button 
            className="excel-btn" 
            onClick={() => setIsExcelModalOpen(true)}
            title="Generate Excel Reports"
          >
            📊
          </button>
        </div>
      </header>
      
      <ExcelReportModal 
        isOpen={isExcelModalOpen} 
        onClose={() => setIsExcelModalOpen(false)} 
      />
    </>
  );
};

export default Header;

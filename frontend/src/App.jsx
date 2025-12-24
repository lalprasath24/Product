import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from "./components/Login/Login";
import Otp_verify from "./components/Login/Otp_verify";
import Main from "./components/Dashboard/Main";
import Customers from "./components/customers/Customers";
import Products from "./components/products/Products";
import Plans from "./components/plans/Plans";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/otp-verify" element={<Otp_verify />} />
        <Route path="/dashboard" element={<Main/>}/>
        <Route path="/customers" element={<Customers/>}/>
        <Route path="/products" element={<Products/>}/>
        <Route path="/plans" element={<Plans/>}/>
      </Routes>
    </Router>
  );
}

export default App;

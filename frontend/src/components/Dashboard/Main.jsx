import React from "react";
import "./Main.css";
import Header from "./Header";
import Fooder from "./Fooder";


const Main = () => {
  return (
    <>
    <Header/>
      {/* <main className="main">
      <h2>Available Milk Packages</h2>
      <div className="cards">
        <div className="card">
          <h3>1 Liter</h3>
          <p>₹50 per pack</p>
          <button>Add to Cart</button>
        </div>
        <div className="card">
          <h3>2 Liters</h3>
          <p>₹95 per pack</p>
          <button>Add to Cart</button>
        </div>
        <div className="card">
          <h3>Monthly Subscription</h3>
          <p>₹1400 per month</p>
          <button>Subscribe</button>
        </div>
      </div>
      </main> */}
      <Fooder/>
    </>

  );
};

export default Main;

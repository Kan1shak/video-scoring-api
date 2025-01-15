import React, { useState,useEffect } from "react";
import { useSharedContext } from "../sharedContext";
import { Link } from "react-router-dom";
import InputForm from "./InputForm";
import Navbar from "./Navbar";
import gsap from "gsap";

const videos = [
  "Final_vedio0001-0579.mp4",
  "WhatsApp Video 2024-12-23 at 05.14.05.mp4",
  "WhatsApp Video 2024-12-22 at 21.55.20.mp4",
  "WhatsApp Video 2024-12-22 at 21.38.54.mp4",
  "WhatsApp Video 2024-12-23 at 21.27.44.mp4",
  "WhatsApp Video 2024-12-23 at 21.27.45.mp4"
];

const videos2 =[
  "https://res.cloudinary.com/dzz1r3hcf/video/upload/v1734982012/xqiavzhjbiuthhts5pvq.mp4",
  "https://res.cloudinary.com/dzz1r3hcf/video/upload/v1734983257/nn2mzuseujljoke5vmgn.mp4",
  "https://res.cloudinary.com/dzz1r3hcf/video/upload/v1734977696/ih9toaqwvj8im6rh6mp4.mp4"

]

const HomePage = () => {

let lastScrollY = 1;
const [showNav, setShowNav] = useState(true);
const [showForm, setShowForm] = useState(false);

addEventListener("scroll", () => {
  if (window.scrollY < lastScrollY) {
    lastScrollY = window.scrollY;
    setShowNav(true);}
  else{
    setShowNav(false);
  }
 
  });

  useEffect(() => {
    gsap.from(".main", {
      duration: 1,
      x: -100,
      opacity: 0,
      ease: "bounce",
      stagger: 0.5
    });
  })
 
  return (
    <div className={`${showForm? 'h-screen overflow-hidden': 'h-full'} Main Scroll w-screen relative bg-no-repeat bg-contain bg-black`}>
      <Navbar showNav={showNav} setShowNav={setShowNav} />
      <div 
      style={{backgroundImage:'url(bg.svg)'
      }}
      className="flex flex-col bg-center bg-no-repeat gap-4 justify-center items-center min-h-screen h-full w-full">
      <div className="gradient text-transparent text-5xl font-bold">
  Discover the Future
</div>

        <p className="text-5xl font-bold z-10 mix-blend-overlay text-white">With Artifiial Intelligence</p>
        <div className="relative bottom-6 bg-transparent flex items-center justify-center">
  <div
  className="absolute w-[500px] shadow-glow animate-glow flex justify-center rounded-full">
</div>
</div>
<p className="text-gray-200 text-center font-medium text-md ">Lorem ipsum dolor sit amet consectetur adipisicing elit. Ipsum optio officiis sit ex architecto?<br></br> Error ipsa natusquis minima debitis quas perspiciatis, dolores aliquam numquam odio <br></br> cum commodi! Reprehenderit, corporis?</p>
 <div className="flex gap-12 mt-5">
        {/* Generate Video Button */}
        <Link to="/input-form">
        <button 
          className="px-6 py-3 bg-gradient-to-r to-[#6f36ac] from-[#7263b0] text-gray-200 font-bold rounded-lg shadow-lg hover:shadow-purple-500/65 transition"
        >
          Generate Video
        </button>
        </Link>

        {/* Remove Background Button */}
        <Link to="/catalogue">
        <button
          className="relative px-6 py-3 overflow-hidden bg-black bg-gradient-to-r from-[#ee9ca7] to-[#ffdde1] border border-gray-400 rounded-full font-medium hover:bg-gradient-to-l hover:from-[#ee9ca7] hover:to-[#ffdde1] hover:text-black transition-colors duration-1000 "
        >
          Collections
        </button>
        </Link>
    </div>
    </div>
    <div className="flex pt-2 bg-opacity-5 bg-black pb-2 justify-between w-screen">
      <div className=" ml-16 flex flex-col gap-4">
      <div className="flex justify-center items-center bg-clip-text bg-gradient-to-r to-[#6f36ac] from-[#7263b0] w-28 h-12 text-white p-2 px-4 rounded-2xl backdrop-blur-lg border border-gray-500 hover:bg-opacity-0 focus:outline-none">
  <h1 className="text-transparent">AI Videos</h1>
  </div>
  <h1 className="text-4xl font-normal  text-white text-start">Generate Ads For <br></br> Your Product ,With AI</h1>
  <p className="text-white text-sm ">Boost your product's reach with AI-generated ads Tailor creative,  <br></br>engaging content that resonates with your audience and <br></br> enhances conversions Let AI power your marketing today!.</p>
  <div className="flex justify-between gap-4">
    <div className="flex w-28 h-28  ml-1 justify-center items-center flex-col gap-4">
        <h1 className="text-xl -ml-2 mt-1 font-normal text-white">AI Generated</h1>
        <img className="w-36 mt-2 h-28"
        src="https://imgs.search.brave.com/GP3Pi1lZXVrFhpK8fWjeux52s-8R1PUtwIXq0NNCX94/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9jZG4u/cHJvZC53ZWJzaXRl/LWZpbGVzLmNvbS82/M2RhMzM2MmY2N2Vk/NmY3MWM5NDg5YzEv/NjcwZmMzODc2YTgx/Yzc1Zjk2NDcxZTUy/XzMtVW5saW1pdGVk/JTIwVmlkZW8lMjBD/cmVhdGlvbi5wbmc"></img>
        </div>
        <div className="flex flex-col gap-4">
        <h1 className="text-xl font-normal text-white">Cost Efficient</h1>
        <img className="ml-6 w-16 h-16"
        src="https://imgs.search.brave.com/LvC69S7m_d-ZgQq9cjfbBWl54ZcQhtqwmD8SEtAMCLU/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly93d3cu/cG5nbWFydC5jb20v/ZmlsZXMvMy9HcmVl/bi1Eb2xsYXItU3lt/Ym9sLVBORy1QaWN0/dXJlLnBuZw"
        >
        </img>
        </div>
       <div className="flex flex-col gap-4">
        <h1 className="text-xl font-normal text-white">Time Saving</h1>
        <img 
        src="https://imgs.search.brave.com/CxcrLEjebNmdxVVNwEroUn98vaMKx8B7rDaaJCw65Yw/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9jZG4t/aWNvbnMtcG5nLmZy/ZWVwaWsuY29tLzI1/Ni8xNzU1MS8xNzU1/MTI3Ny5wbmc_c2Vt/dD1haXNfaHlicmlk"
        className="ml-6 w-16 h-16">
        </img>
        </div>
        </div>
      </div>
      <div className="flex relative mr-16 rounded-xl w-[40%] border-2 border-gray-600">
      <div className= 'absolute top-[55%] rounded-xl -left-20 border-2 border-gray-400 w-[30%] h-[30%]'>
      <video
      muted
      autoPlay
      loop
      className="w-[100%] h-[100%] rounded-xl"
      src="https://res.cloudinary.com/dzz1r3hcf/video/upload/v1735026699/war4lxeqzycvrhid5jzp.mp4"
      >

      </video>
      </div>
      <video
      muted
      autoPlay
      loop
      className="rounded-xl"
      src="https://res.cloudinary.com/dzz1r3hcf/video/upload/v1734989182/cedt1uyggybc3rc1qqun.mp4"
      ></video>
      </div>
      </div>
      <div className="flex bg-black justify-center items-center gap-4 flex-col pt-20">
      <div className="flex bg-gradient-to-r from-[#ee9ca7] to-[#ffdde1] bg-clip-text justify-center items-center bg-opacity-5 w-28 h-12 p-2 px-4 rounded-2xl backdrop-blur-lg border border-gray-500 hover:bg-opacity-0 focus:outline-none">
  <h1 className="text-transparent"> AI Photos </h1>
  </div>
  <div className="flex justify-center items-center text-center flex-col ">
  <h1 className="text-4xl font-normal text-white text-center">AI Generated Photos <br></br> For Your Business</h1>
  <div className="bg-clip-text bg-gradient-to-r from-[#ee9ca7] to-[#ffdde1]">
    <p className=" text-md text-transparent mt-4">AI-generated photos provide customized, high-quality visuals for <br></br> businesses saving time and costs while enhancing  branding, <br></br> marketing, and engagement effortlessly.</p>
    </div>
  <div className="flex justify-around items-center pt-10 w-screen h-full gap-4">
  <div className="p-2 bg-black border-2 border-gray-500 rounded-2xl">
  <img className="w-[370px] border-2 border-slate-700 h-64 rounded-2xl" 
  src="https://res.cloudinary.com/dzz1r3hcf/image/upload/v1735450939/amozdnqtwvzgarhyzoha.png"></img>
  </div>
  <div className="p-2 bg-black border-2 border-gray-500 rounded-2xl">
  <img className="w-[370px] border-2 border-slate-700 h-64 rounded-2xl"
  src="https://res.cloudinary.com/dzz1r3hcf/image/upload/v1736616288/svhucaguczhmfdldcayl.png"></img>
  </div>
  <div className="p-2 bg-black border-2 border-gray-500 rounded-2xl">
  <img  
  className="w-[370px] h-64 border-2 border-slate-700 rounded-2xl"
  src="https://res.cloudinary.com/dzz1r3hcf/image/upload/v1734990540/yon9tv7o9yogchl8mqcr.png"></img>
  </div>
    </div>
  </div>
      </div>
      <div className="flex justify-center items-center">
      <div className="flex styled-div w-screen mt-24 pb-24">

        </div>
        </div>   
    </div>
  );
};

export default HomePage;

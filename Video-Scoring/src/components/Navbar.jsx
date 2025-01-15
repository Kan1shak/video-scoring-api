import React from 'react'
import { useState } from "react";
import PropTypes from 'prop-types';
import { Link } from 'react-router-dom';

export default function Navbar( {showNav, setShowNav} ) {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <>
    {(showNav &&<nav className="bg-black fixed z-999 bg-opacity-5 w-screen flex h-20 justify-center items-center p-4">
      <div className="ml-2 container relative flex bg-white backdrop-blur-sm bg-opacity-10 w-[40%] h-12 rounded-full justify-center items-center">        
        <div className="flex w-full justify-around items-center md:flex">
          <Link to={"/"}>
          <h1  className="text-white hover:text-gray-200">
            Home
          </h1>
          </Link>
          <Link to={"/input-form"}>
          <h1 href="#about" className="text-white hover:text-gray-200">
            Generate
          </h1>
          </Link>
          <Link to={"/catalogue"}>
          <a href="#contact" className="text-white hover:text-gray-200">
            Collections
          </a>
          </Link>
        </div>
        <div
          className="md:hidden text-white cursor-pointer"
          onClick={() => setIsOpen(!isOpen)}
        >
          <span className="text-2xl">&#9776;</span>
        </div>
      </div>
      {/* Mobile Menu */}
      {isOpen && (
        <div className="md:hidden bg-blue-600">
          <a
            href="#home"
            className="block text-white py-2 px-4 hover:bg-blue-700"
          >
            Home
          </a>
          <a
            href="#about"
            className="block text-white py-2 px-4 hover:bg-blue-700"
          >
            Generate
          </a>
          <a
            href="#contact"
            className="block text-white py-2 px-4 hover:bg-blue-700"
          >
            Catalogue
          </a>
        </div>
      )}
    </nav>
  )}
  </>
  );
}
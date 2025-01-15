// SharedContext.js
import React, { createContext, useState, useContext } from 'react';
import PropTypes from 'prop-types'; // Import PropTypes for prop validation

const SharedContext = createContext();

export const useSharedContext = () => {
  const context = useContext(SharedContext);
  if (!context) {
    throw new Error('useSharedContext must be used within a SharedProvider');
  }
  return context;
};


export const SharedProvider = ({ children }) => {
  const [inputData, setInputData] = useState({});  
  const [outputData, setOutputData] = useState({});
  
  

  const updateInputData = (newValue) => {
    setInputData(newValue);
  };


  const updateOutputData = (newValue) => {
    setOutputData(newValue);
    console.log(outputData)
  };

  return (
    <SharedContext.Provider value={{ inputData, outputData, updateInputData, updateOutputData }}>
      {children}
    </SharedContext.Provider>
  );
};


SharedProvider.propTypes = {
  children: PropTypes.node.isRequired, 
};

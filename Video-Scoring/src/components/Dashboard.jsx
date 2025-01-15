import React from 'react';
import { useState } from 'react';
import { useSharedContext } from '../sharedContext';
import { useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Link } from 'react-router-dom';

const Dashboard = () => {

  const {id} = useParams();
  const [count,setCount] = useState(0)
  const [minutes, setMinutes] = useState(15);
  const [seconds, setSeconds] = useState(0);
  const [isRunning, setIsRunning] = useState(false); 
  const [isSuccess, setIsSuccess] = useState(false);
  const [scoringCriteria, setScoringCriteria] = useState([]);
  const { inputData, outputData,updateInputData,updateOutputData } = useSharedContext();
  const [getJustifictaions,setGetJustifications] = useState(false)
  const [justifications,setJustifications] = useState([]) 


  useEffect(() => {
  if(inputData.scoring_criteria){
  setScoringCriteria(Object.entries(inputData.scoring_criteria).map(([key, value]) => ({
    name: key,
    value: value
  })))
  console.log(scoringCriteria)
}},[])

  useEffect(()=>{
  if(outputData.video_url){
    setIsRunning(false);
    setIsSuccess(true)
  }
  else if(!outputData.isSucessful){
    setIsSuccess(false)
    setIsRunning(false);
  }
  else {
    setIsRunning(true)
  }
},[outputData])

  useEffect(() => {
    let timerInterval;
    if (isRunning) {
      timerInterval = setInterval(() => {
        setSeconds((prevTime) => prevTime - 1)
        setCount((prev)=>prev+1);
      }, 1000);
    }
    if(seconds < 0){
      setSeconds(59);
      setMinutes((prevTime) => prevTime - 1);
    }
    return () => clearInterval(timerInterval);
  }, [isRunning,seconds]); 


 useEffect(() => {
  const fetchData = async()=>{

   if(id===' ') return 
  const response = await fetch(`https://kanishak-video-scoring-api.hf.space/score-video/${id}/`,{method:'GET'})
  console.log(response);
  if(response.ok){
    const data = await response.json();
    console.log(data);
    updateOutputData(data);
  }
  else{
    console.log(`https://kanishak-video-scoring-api.hf.space/score-video/${id}`)
  }
 }
fetchData();
},[])

const getScoreBreakdown = ()=>{
setJustifications(Object.entries(outputData.scoring.justifications).map(([id, value]) => ({
  id,
  value
})))
console.log(justifications)
setGetJustifications(!getJustifictaions)
}

const convertToFilteredArray = (data) => {
  setScoringCriteria(Object.entries(data.scoring)
    .filter(([key]) => key !== "justifications")
    .map(([key, value]) => ({ name: key, score: value })));
    console.log(scoringCriteria)
};

function toTitleCase(str) {
  return str.replace(
    /\w\S*/g,
    text => text.charAt(0).toUpperCase() + text.substring(1).toLowerCase()
  );
}


useEffect(()=>{
if(outputData.scoring){
  convertToFilteredArray(outputData)
}},[outputData])


  return (
    <>
    <div className="p-6 overflow-hidden relative bg-black min-h-screen">
      <div className="flex justify-between items-center bg-gray-800 p-4 rounded-md shadow-md">
        <div className="flex space-x-4 justify-between w-full">
          <Link to={'/'}>
        <button className="px-4 py-2 bg-gray-900 text-white rounded-md">Back</button>
        </Link>
          <div className="flex space-x-4">
          <button 
          className="px-4 py-2 bg-green-500 border-2 border-gray-600 text-white rounded-md">Video</button>
          <button className="px-4 py-2 bg-gray-900 text-white rounded-md">Scoring</button>
          <button className="px-4 py-2 bg-gray-900 text-white rounded-md">Download</button>
          </div>
        </div>
      </div>

      <div className="mt-6 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div className="bg-gray-800 p-4 rounded-md shadow-md col-span-2">
          <div className="w-full relative aspect-video bg-gray-900 rounded-md flex items-center justify-center">
            <span className="text-gray-500">
            {!isRunning? isSuccess? (<video className=''
            loop
            controls
            autoPlay
            muted
            src={outputData.video_url}
            ></video>):(<img 
            className='w-64 h-64'
            src='https://res.cloudinary.com/dzz1r3hcf/image/upload/v1736792704/snaixkgorcx9jhqdt8i1.png'></img>)
            :(<img 
              className='w-64 h-64'
              src='https://media.tenor.com/Y7bSnLM1Cw8AAAAj/bar-penguin.gif'></img>)}
            </span>
            {outputData.video_url? '':<p className='absolute right-5  bottom-5 text-white'>Time Left ≈ {minutes} m : {seconds} s</p>}
          </div>
          <div className="mt-4 flex items-center justify-between">
            <h2 className="text-lg font-bold text-white">Video Generation</h2>
            <span className={`px-3 py-1 ${isRunning?'bg-yellow-500':isSuccess?'bg-green-500':'bg-red-500'} text-white rounded-full`}>{isRunning? 'Generating':isSuccess?'Success':'Failed'}</span>
          </div>
        </div>

        {/* Metrics Section */}
        <div className="bg-gray-800 relative p-4 rounded-md shadow-md">
          <h2 className="text-lg font-bold mb-4 text-white">Metrics</h2>
          <div className=" grid grid-cols-3 gap-4">
            </div>
            <div className="grid grid-cols-3 gap-6">

  {scoringCriteria.map((criteria, index) => (
    <div
      key={index}
      className="flex flex-col justify-center items-center"
    >
      <div
        onClick={() => handleVisible("critera")}
        className={`${
           "bg-green-100"
        } w-12 h-12 rounded-full flex items-center justify-center`}
      >
        {outputData.video_url || inputData ? (
          <span
            className={`${
             "text-green-600"
            }`}
          >
           {criteria.score?criteria.score:(<img className='w-6 h-6'
           src='https://media.tenor.com/szH2qsISnzMAAAAj/emoji-thinking.gif'
           ></img>)}
          </span>
        ) : (
          <img
            className="w-6 h-6"
            src="https://media.tenor.com/2fE4s1GXDNEAAAAj/loading.gif"
          ></img>
        )}
      </div>
      <p className="text-sm text-center text-white mt-2 overflow-hidden w-full text-ellipsis line-clamp-2">
        {criteria.name
          .replaceAll("_", " ")
          .toLowerCase()
          .replace(/\b\w/g, (char) => char.toUpperCase())}
      </p>
    </div>
  ))}
  
</div>
            </div>
          </div>
          {outputData.video_url && (<p className='text-xl absolute bottom-32 right-14  text-white'>Total Time Taken : {(count/60).toFixed(2)} mintues </p>)}
          {outputData.video_url && (<button 
          onClick={getScoreBreakdown}
          className='justification-button text-xl absolute bottom-10 right-10  text-white'>{getJustifictaions?'Click To Hide Score Breakdown':'Click To Get Score Breakdown'}</button>)}
        </div>
        {getJustifictaions &&( <div className="justifications-container">
        
          {justifications.map((criteria, index) => (
          <div key={index} className='justifications-card'>
              <h1 className='text-white justificationId'>{toTitleCase(criteria.id.replaceAll('_',' '))}</h1>
              <h1 className='text-white justificationValue'>{criteria.value}</h1>
          </div>
        ))}
        </div>)}
        </>
      
  );
};

export default Dashboard;

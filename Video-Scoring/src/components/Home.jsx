import React, { useState } from "react";
import { useSharedContext } from "../sharedContext";
import { Link } from "react-router-dom";

const videos = [
  "Final_vedio0001-0579.mp4",
  "Final_vedio0001-0579.mp4",
  "Final_vedio0001-0579.mp4",
  "Final_vedio0001-0579.mp4",
  "Final_vedio0001-0579.mp4"
];

const HomePage = () => {
  const { inputData,outputData,updateInputData,updateOutputData } = useSharedContext();
  const [showOverlay, setShowOverlay] = useState(false)
  const [count, setCount] = useState(1)
  const [product, setProduct] = useState('')
  const [tagline,setTagline] = useState('')
  const [brandPallete,setBrandPallete] = useState([])
  const [height, setHeight] = useState(0)
  const [width,setWidth] = useState(0)
  const [CTA,setCTA] = useState('')
  const [Logo, setLogo] = useState('')
  const [Video, setVideo] = useState('')
  const [Duration, setDuration] = useState(0)
  const [BGFG, setBgSeperation] = useState(0)
  const [BrandAdherence, setBrandAdherence] = useState(0)
  const [VisualAppeal, setVisualAppeal] = useState(0)
  const [ProductFocus, setProductFocus] = useState(0)
  const [CallToAction, setCallToAction] = useState(0)
  const [AudienceRelevance, setAudienceRelevance] = useState(0)

  async function scoreVideo(videoDetails, scoringCriteria) {
  const url = 'https://kanishak-video-scoring-api.hf.space/score-video';  

  
  const requestBody = {
    video_details: videoDetails,
    scoring_criteria: scoringCriteria,
  };

  updateInputData(requestBody)  

  console.log('Request Body:', requestBody);

  try {
    const response = await fetch(url, {
      method: 'POST',  
      headers: {
        'Content-Type': 'application/json',  
      },
      body: JSON.stringify(requestBody), 
    });

    if (!response.ok) {
      throw new Error(`Error: ${response.statusText}`);
    }

    const data = await response.json();
    console.log('Scoring Result:', data);
    updateOutputData(data)
    console.log('Output Data:', outputData);
  } catch (error) {
    console.error('Request failed:', error);
  }
}
  function Submit(){
    setShowOverlay(true);
    
     const videoDetails = {
        "product_name": product,
        "tagline": tagline,
        "brand_palette": brandPallete,
        "dimensions": {
          "width": width,
          "height": height
        },
        "duration": Duration,
        "cta_text": CTA,
        "logo_url": Logo,
        "product_video_url": Video
      }

      const scoringCriteria = {
        "background_foreground_separation": BGFG,
        "brand_guideline_adherence": BrandAdherence,
        "creativity_visual_appeal": VisualAppeal,
        "product_focus": ProductFocus,
        "call_to_action": CallToAction,
        "audience_relevance": AudienceRelevance
      }
      
      scoreVideo(videoDetails, scoringCriteria)
    
  }
  const [showForm, setShowForm] = useState(false);

 
  return (
    <div className={`${showForm? 'h-screen overflow-hidden': 'h-full'} overflow-x-hidden`}>
    <div className={`${showForm? ' overflow-hidden':''} h-full  flex flex-col w-full justify-between items-start bg-gray-100 text-gray-200`}
    style={{backgroundImage:"url('pexels-goldcircuits-2425232.jpg')", backgroundSize:"cover", backgroundPosition:"center", backgroundRepeat:"no-repeat"}}
    >
        <div className="flex  ml-16 gap-28 justify-between w-1/3 h-screen">
        <div className="flex flex-col items-center gap-4">
        <div className="relative w-0.5 bg-zinc-900 h-56">
        <div className="absolute  top-0 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-5 h-5 bg-gray-400 rounded-full border-4 border-gray-800">
        </div>
        <div className="absolute bottom-0 left-1/2 transform -translate-x-1/2 w-6 h-6 border-2 border-gray-800 rounded-full"></div>
      </div>
      <div className="flex bg-[url('pexels-fwstudio-33348-129733.jpg')] items-center justify-center h-40 w-48 text-white rounded-lg shadow-lg">
      <h1 className="text-2xl font-bold uppercase">Generate</h1>
    </div>
      </div>
      <div className="flex flex-col items-center gap-4">
        <div className="relative w-0.5 bg-zinc-900 h-[430px]">
        <div className="absolute  top-0 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-5 h-5 bg-gray-400 rounded-full border-4 border-gray-800">
        </div>
        <div className="absolute bottom-0 left-1/2 transform -translate-x-1/2 w-6 h-6 border-2 border-gray-800 rounded-full"></div>
      </div>
      <div className="flex bg-[url('pexels-fwstudio-33348-172276.jpg')] items-center justify-center h-40 w-48 text-white rounded-lg shadow-lg">
      <h1 className="text-2xl font-bold uppercase">Your</h1>
    </div>
      </div>
      <div className="flex flex-col items-center gap-4">
        <div className="relative w-0.5 bg-zinc-900 h-72">
        <div className="absolute  top-0 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-5 h-5 bg-gray-400 rounded-full border-4 border-gray-800">
        </div>
        <div className="absolute bottom-0 left-1/2 transform -translate-x-1/2 w-6 h-6 border-2 border-gray-800 rounded-full"></div>
      </div>
      <div className="flex bg-[url('pexels-fwstudio-33348-163999.jpg')] items-center justify-center h-40 w-48 text-white rounded-lg shadow-lg">
      <h1 className="text-2xl font-bold uppercase">Own</h1>
    </div>
      </div>
      <div className="flex flex-col items-center gap-4">
        <div className="relative w-0.5 bg-zinc-900 h-32">
        <div className="absolute  top-0 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-5 h-5 bg-gray-400 rounded-full border-4 border-gray-800">
        </div>
        <div className="absolute bottom-0 left-1/2 transform -translate-x-1/2 w-6 h-6 border-2 border-gray-800 rounded-full"></div>
      </div>
      <div className="flex bg-[url('pexels-fwstudio-33348-129723.jpg')] transform rotate-12 items-center justify-center h-40 w-48 text-black rounded-lg shadow-lg">
      <h1 className="text-2xl mix-blend-multiply font-semibold uppercase">Product</h1>
    </div>
      </div>
      <div className="flex flex-col items-center gap-4">
        <div className="relative w-0.5 bg-zinc-900 h-96">
        <div className="absolute  top-0 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-5 h-5 bg-gray-400 rounded-full border-4 border-gray-800">
        </div>
        <div className="absolute bottom-0 left-1/2 transform -translate-x-1/2 w-6 h-6 border-2 border-gray-800 rounded-full"></div>
      </div>
      <div className="flex bg-[url('pexels-fwstudio-33348-132193.jpg')] items-center justify-center h-40 w-48 text-white rounded-lg shadow-lg">
      <h1 className="text-2xl font-bold uppercase">Ad</h1>
    </div>
      </div>
    </div>
    <div className="flex mb-8 w-screen h-screen gap-28 flex-col">
    <div className="overflow-hidden relative w-full  h-full bg-transparent">
      <div className="flex w-[calc(300px*3)] gap-16 animate-scroll">
        {videos.concat(videos).map((video, index) => (
          <div key={index} className="w-[400px] flex-shrink-0 ">
            <video
              src={video}
              className="w-full rounded-xl h-full object-cover"
              loop
              autoPlay
              muted
            />
          </div>
        ))}
      </div>
    </div>
    <div className="overflow-hidden relative w-full h-full bg-transparent">
      <div className="flex justify-center w-[calc(300px*3)] gap-16 animate-reverse">
        {videos.concat(videos).map((video, index) => (
          <div key={index} className="w-[400px] flex-shrink-0 ">
            <video
              src={video}
              className="w-full rounded-xl h-full object-cover"
              loop
              autoPlay
              muted
            />
          </div>
        ))}
      </div>
    </div>
    <div className="flex w-screen justify-center items-center">
    <button 
    onClick={() => setShowForm(!showForm)}
    className="h-14 w-42 px-8 py-3 text-lg font-semibold text-white bg-gradient-to-r from-purple-600 via-purple-700 to-purple-800 rounded-lg shadow-lg transition-all duration-300 ease-in-out hover:shadow-purple-400/80 hover:-translate-y-1">
      <span className="absolute inset-0 bg-gradient-to-r from-white/10 to-transparent rounded-lg blur-md -z-10"></span>
      Get Started
    </button>
    </div>
        </div>
        <div>
          </div>
          </div>
            <div 
            style={{backgroundImage:"url('pexels-knownasovan-62693.jpg')"}}
            className={` ${
              showForm
                ? "translate-y-0 opacity-100 overflow-y-scroll"
                : "-translate-y-full opacity-0"
            } transition-all duration-700 fixed inset-0 overflow-x-hidden overflow-y-scroll flex flex-col bg-center bg-cover items-center justify-center h-full`}>
              <div 
              onClick={() => setShowForm(false)}
              className="absolute cursor-pointer bg-blue-500 size-8 top-10 text-center text-2xl right-10 rounded-full">X</div>
          <div className=' m-6 border-t-2 border-gray-900 h-full min-h-screen gap-16 flex items-start justify-between'>
            <div className= " mt-5 flex flex-col w-1/3 justify-center items-center">
            <div className="relative w-0.5 bg-zinc-900 h-56">
              <div className="absolute  top-0 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-5 h-5 bg-gray-500 rounded-full border-4 border-gray-800">
              </div>
              <div className="absolute bottom-0 left-1/2 transform -translate-x-1/2 w-6 h-6 border-2 border-gray-900 rounded-full"></div>
            </div>
          <div className="flex justify-center items-center h-1/2 rounded-xl">
            <div className="w-full p-6 bg-zinc-900 rounded-xl shadow-lg shadow-zinc-700 border-t-2 border-l-2 border-fuchsia-700">
              <h2 className="text-2xl font-semibold text-gray-200 mb-4 text-center">
                Enter your product Details
              </h2>
              <label className="m-2 text-gray-200 font-semibold" htmlFor="product-name">Product Name</label>
                <input
                  onChange={(e) => setProduct(e.target.value)}
                  label="Product Name"
                  type="text"
                  placeholder="Enter Product Name"
                  className="w-full p-3 mb-4 text-black bg-gray-100 border border-gray-800 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <label className="m-2 text-gray-200 font-semibold" htmlFor="Tagline">Product Tagline</label>
                <input
                onChange={(e) => setTagline(e.target.value)}
                  label="Tagline"
                  type="text"
                  placeholder="Enter Product Tagline"
                  className="w-full p-3 mb-4 text-black bg-gray-100 border border-gray-800 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <div className='flex justify-between'>
                <label className="m-2 text-gray-200 font-semibold" htmlFor="brand pallete">Brand Pallete</label>
                <div className='flex gap-2'>
                <button
                onClick={() => setCount(count + 1)}
                className="w-16 h-8 mb-2 py-1 text-black bg-gray-400 rounded-lg hover:bg-gray-600 focus:ring-2 focus:ring-gray-400 focus:outline-none"
              >
                Add
              </button>
              <button
                onClick={() => count>1? setCount(count - 1):null}
                className="w-16 h-8 mb-2 py-1 text-black bg-gray-400 rounded-lg hover:bg-gray-600 focus:ring-2 focus:ring-gray-400 focus:outline-none"
              >
                Del
              </button>
              </div>
                </div>
                {Array.from({ length: count }).map((_, i) => (
              <input
              onChange={(e) => {
                const updatedPalette = [...brandPallete];
                updatedPalette[i] = e.target.value;
                setBrandPallete(updatedPalette);
              }}
                key={i}
                label={`Brand Palette ${i + 1}`}
                type="text"
                placeholder={`Enter Color's Hex Code`}
                className="w-full p-3 mb-4 text-black bg-gray-100 border border-gray-800 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            ))}
            </div>
          </div>
            </div>
            <div className= " mt-5 flex flex-col w-1/3 justify-center items-center">
            <div className="relative w-0.5 bg-zinc-900 h-56">
              <div className="absolute  top-0 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-5 h-5 bg-gray-400 rounded-full border-4 border-gray-800">
              </div>
              <div className="absolute bottom-0 left-1/2 transform -translate-x-1/2 w-6 h-6 border-2 border-gray-800 rounded-full"></div>
            </div>
            <div className="flex justify-center items-center h-1/2 rounded-xl">
            <div className="w-full p-6 bg-zinc-900 rounded-xl shadow-lg border-t-2 border-l-2 border-fuchsia-700">
              <h2 className="text-2xl font-semibold text-gray-200 mb-4 text-center">
                Enter Video Dimensions
              </h2>
              <label className="m-2 text-gray-200 font-semibold" htmlFor="product-name">Video Height</label>
                <input
                  onChange={(e) => setHeight(parseInt(e.target.value))}
                  type="number"
                  placeholder="Product Name"
                  className="w-full p-3 mb-4 text-black bg-gray-100 border border-gray-800 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <label className="m-2 text-gray-200 font-semibold" htmlFor="product-name">Video Width</label>
                <input
                onChange={(e) => setWidth(parseInt(e.target.value))}
                  type="number"
                  placeholder="Product Name"
                  className="w-full p-3 mb-4 text-black bg-gray-100 border border-gray-800 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
            </div>
          </div>
            </div>
            <div className= " mt-5 flex flex-col w-1/3 justify-center items-center">
            <div className="relative w-0.5 bg-zinc-900 h-56">
              <div className="absolute  top-0 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-5 h-5 bg-gray-400 rounded-full border-4 border-gray-800">
              </div>
              <div className="absolute bottom-0 left-1/2 transform -translate-x-1/2 w-6 h-6 border-2 border-gray-800 rounded-full"></div>
            </div>
            <div className="flex justify-center items-center h-1/2 rounded-xl">
            <div className="w-full p-6 bg-zinc-900 rounded-xl shadow-lg border-t-2 border-l-2 border-fuchsia-700">
              <h2 className="text-2xl font-semibold text-gray-200 mb-4 text-center">
                Enter Video Details
              </h2>
              <label className="m-2 text-gray-200 font-semibold" htmlFor="Tagline">CTA Text</label>
                <input
                onChange={(e) => setCTA(e.target.value)}
                  type="text"
                  placeholder="Enter Call To Action"
                  className="w-full p-3 mb-4 text-black bg-gray-100 border border-gray-800 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                 <label className="m-2 text-gray-200 font-semibold" htmlFor="Tagline">Logo URL</label>
                <input
                onChange={(e) => setLogo(e.target.value)}
                  type="url"
                  placeholder="Enter Logo Url"
                  className="w-full p-3 mb-4 text-black bg-gray-100 border border-gray-800 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                 <label className="m-2 text-gray-200 font-semibold" htmlFor="Tagline">Video URL</label>
                <input
                onChange={(e) => setVideo(e.target.value)}
                  type="url"
                  placeholder="Enter Video Url"
                  className="w-full p-3 mb-4 text-black bg-gray-100 border border-gray-800 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                 <label className="m-2 text-gray-200 font-semibold" htmlFor="Tagline">Duration</label>
                 <input
                 onChange={(e) => setDuration(parseInt(e.target.value))}
                  type="number"
                  placeholder="Enter Video Duration"
                  className="w-full p-3 mb-4 text-black bg-gray-100 border border-gray-800 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
            </div>
          </div>
            </div>
            <div className= " mt-5 flex flex-col w-1/3 justify-center items-center">
            <div className="relative w-0.5 bg-zinc-900 h-56">
              <div className="absolute  top-0 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-5 h-5 bg-gray-400 rounded-full border-4 border-gray-800">
              </div>
              <div className="absolute bottom-0 left-1/2 transform -translate-x-1/2 w-6 h-6 border-2 border-gray-800 rounded-full"></div>
            </div>
            <div className="flex justify-center items-center h-1/2 rounded-xl">
            <div className="w-full p-6 bg-zinc-900 rounded-xl shadow-lg border-t-2 border-l-2 border-fuchsia-700">
              <h2 className="text-2xl font-semibold text-gray-200 mb-4 text-center">
                Enter Scoring Criteria
              </h2>
              <div className='flex flex-col gap-8'>
              <div className='flex items-center justify-between'> 
                <label className="m-2 text-gray-200 font-semibold" htmlFor="Tagline">BG-FG Seperation</label>
                 <input
                 onChange={(e) => setBgSeperation(parseInt(e.target.value))}
                  type="number"
                  placeholder="Max Score"
                  className="w-32 p-3 text-black bg-gray-100 border border-gray-800 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                </div>
                <div className='flex items-center justify-between'> 
                <label className="m-2 text-gray-200 font-semibold" htmlFor="Tagline">Brand Adherence</label>
                 <input
                  onChange={(e) => setBrandAdherence(parseInt(e.target.value))}
                  type="number"
                  placeholder="Max Score"
                  className="w-32 p-3 text-black bg-gray-100 border border-gray-800 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                </div>
                <div className='flex items-center justify-between'> 
                <label className="m-2 text-gray-200 font-semibold" htmlFor="Tagline">Visual Appeal</label>
                 <input
                  onChange={(e) => setVisualAppeal(parseInt(e.target.value))}
                  type="number"
                  placeholder="Max Score"
                  className="w-32 p-3 text-black bg-gray-100 border border-gray-800 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                </div>
                 <div className='flex items-center justify-between'> 
                <label className="m-2 text-gray-200 font-semibold" htmlFor="Tagline">Product Focus</label>
                 <input
                 onChange={(e) => setProductFocus(parseInt(e.target.value))}
                  type="number"
                  placeholder="Max Score"
                  className="w-[120px] p-3 text-black bg-gray-100 border border-gray-800 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                </div>
                 <div className='flex items-center justify-between'> 
                <label className="m-2 text-gray-200 font-semibold" htmlFor="Tagline">Call To Action</label>
                 <input
                 onChange={(e) => setCallToAction(parseInt(e.target.value))}
                  type="number"
                  placeholder="Max Score"
                  className="w-[120px] p-3 text-black bg-gray-100 border border-gray-800 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                </div>
                <div className='flex items-center justify-between'> 
                <label className="m-2 text-gray-200 font-semibold" htmlFor="Tagline">Audience Relevance</label>
                 <input
                 onChange={(e) => setAudienceRelevance(parseInt(e.target.value))}
                  type="number"
                  placeholder="Max Score"
                  className="w-[120px] p-3 text-black bg-gray-100 border border-gray-800 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                </div>
                </div>
            </div>
          </div>
            </div>
          </div>
          <Link to="/dashboard">
          <button
        onClick={Submit}
        type="submit"
        className="relative mb-6 inline-flex items-center justify-center w-32 px-8 py-4 overflow-hidden font-medium text-white transition-all duration-300 bg-gradient-to-r from-indigo-700 to-purple-800 rounded-xl shadow-lg hover:shadow-purple-800/70 group"
      >
        <span className="absolute inset-0 w-32 h-full transition-transform translate-x-0 translate-y-0 bg-gradient-to-br from-gray-700 via-indigo-900 to-black opacity-75 group-hover:translate-y-full group-hover:translate-x-full"></span>
        <span className="relative">Generate</span>
      </button>
      </Link>
       {/* Video Overlay */}
       {showOverlay && (
              <div 
              onClick={() => showOverlay?setShowOverlay(false):null}
              className=" fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50">
                <img src='https://media.tenor.com/vRHC2Oxk45MAAAAi/gunpoint-pointing-gun-at-you.gif' className="w-64 h-64" alt="React Logo" />
              </div>
            )}
        </div>
          </div>
  );
};

export default HomePage;

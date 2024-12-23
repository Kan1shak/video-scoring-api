import React from 'react';
import { useSharedContext } from '../sharedContext';

const Dashboard = () => {

  const [key,setKey] = React.useState('');
  const [visible, setVisible] = React.useState(false);
  const { inputData, outputData } = useSharedContext();

  console.log("OutputData:" ,outputData);
  console.log("InputData:", inputData);

  const handleVisible = (key) => {
    setVisible(true);
    setKey(key);
    console.log(key);
  }



  return (
    <div className="p-6 relative bg-gray-900 min-h-screen">
      <div className="flex justify-between items-center bg-gray-800 p-4 rounded-md shadow-md">
        <div className="flex space-x-4">
          <button className="px-4 py-2 bg-green-500 text-white rounded-md">Video</button>
          <button className="px-4 py-2 bg-gray-900 text-white rounded-md">Scoring</button>
          <button className="px-4 py-2 bg-gray-900 text-white rounded-md">Metrics</button>
          <button className="px-4 py-2 bg-gray-900 text-white rounded-md">Download</button>
          <button className="px-4 py-2 bg-gray-900 text-white rounded-md">Actions</button>
        </div>
      </div>

      <div className="mt-6 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div className="bg-gray-800 p-4 rounded-md shadow-md col-span-2">
          <div className="w-full aspect-video bg-gray-900 rounded-md flex items-center justify-center">
            <span className="text-gray-500">
            <video className=''
            loop
            controls
            autoPlay
            muted
            src={outputData.video_url}
            ></video>
            </span>
          </div>
          <div className="mt-4 flex items-center justify-between">
            <h2 className="text-lg font-bold text-white">Video Generation</h2>
            <span className="px-3 py-1 bg-green-500 text-white rounded-full">Success</span>
          </div>
        </div>

        {/* Metrics Section */}
        <div className="bg-gray-800 p-4 rounded-md shadow-md">
          <h2 className="text-lg font-bold mb-4 text-white">Metrics</h2>
          <div className="grid grid-cols-3 gap-4">
            <div className="flex flex-col items-center">
              <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center">
                <span className="text-green-600">100</span>
              </div>
              <span className="text-sm text-white mt-2">Success</span>
            </div>
            <div className="flex flex-col items-center">
              <div 
              onClick={()=>handleVisible("background_foreground_separation")}
              className={` ${(outputData?.scoring?.background_foreground_separation/inputData?.scoring_criteria?.background_foreground_separation*100)<30?'bg-red-100':
                (outputData?.scoring?.background_foreground_separation/inputData?.scoring_criteria?.background_foreground_separation*100)<70?
                'bg-yellow-100':'bg-green-100'} w-12 h-12 rounded-full flex items-center justify-center`}>
                <span className={`${(outputData?.scoring?.background_foreground_separation/inputData?.scoring_criteria?.background_foreground_separation*100)<30?'text-red-600':
                  (outputData?.scoring?.background_foreground_separation/inputData?.scoring_criteria?.background_foreground_separation*100)<70?
                  'text-yellow-600':'text-green-600'}`}>{(outputData?.scoring?.background_foreground_separation
/inputData?.scoring_criteria?.background_foreground_separation*100).toFixed(1)}</span>
              </div>
              <span className="text-sm text-white mt-2">BG seperation</span>
            </div>
            <div className="flex flex-col items-center">
              <div
              onClick={()=>handleVisible("product_focus")}
              className={`${(outputData?.scoring?.product_focus/inputData?.scoring_criteria?.product_focus*100)<30?'bg-red-100':
                (outputData?.scoring?.product_focus/inputData?.scoring_criteria?.product_focus*100)<70?
                'bg-yellow-100':'bg-green-100'} w-12 h-12 bg-green-100 rounded-full flex items-center justify-center`}>
                <span className={`${(outputData?.scoring?.product_focus/inputData?.scoring_criteria?.product_focus*100)<30?'text-red-600':
                  (outputData?.scoring?.product_focus/inputData?.scoring_criteria?.product_focus*100)<70?
                  'text-yellow-600':'text-green-600'}`}>{(outputData?.scoring?.product_focus
/inputData?.scoring_criteria?.product_focus*100).toFixed(1)}</span>
              </div>
              <span className="text-sm text-white mt-2">Product Focus</span>
            </div>
            <div className="flex flex-col items-center">
              <div 
              onClick={()=>handleVisible("creativity_visual_appeal")}
              className={`${(outputData?.scoring?.creativity_visual_appeal/inputData?.scoring_criteria?.creativity_visual_appeal*100)<30?'bg-red-100':
                (outputData?.scoring?.creativity_visual_appeal/inputData?.scoring_criteria?.creativity_visual_appeal*100)<70?
                'bg-yellow-100':'bg-green-100'} w-12 h-12 bg-green-100 rounded-full flex items-center justify-center`}>
                <span className={`${(outputData?.scoring?.creativity_visual_appeal/inputData?.scoring_criteria?.creativity_visual_appeal*100)<30?'text-red-600':
                  (outputData?.scoring?.creativity_visual_appeal/inputData?.scoring_criteria?.creativity_visual_appeal*100)<70?
                  'text-yellow-600':'text-green-600'}`}>{(outputData?.scoring?.creativity_visual_appeal
/inputData?.scoring_criteria?.creativity_visual_appeal*100).toFixed(1)}</span>
              </div>
              <span className="text-sm text-white mt-2">Visual Appeal</span>
            </div>
            <div className="flex flex-col items-center">
              <div 
              onClick={()=>handleVisible("call_to_action")}
              className={` ${(outputData?.scoring?.call_to_action/inputData?.scoring_criteria?.call_to_action*100)<30?'bg-red-100':
                (outputData?.scoring?.call_to_action/inputData?.scoring_criteria?.call_to_action*100)<70?
                'bg-yellow-100':'bg-green-100'} w-12 h-12 bg-green-100 rounded-full flex items-center justify-center`}>
                <span className={`${(outputData?.scoring?.call_to_action/inputData?.scoring_criteria?.call_to_action*100)<30?'text-red-600':
                  (outputData?.scoring?.call_to_action/inputData?.scoring_criteria?.call_to_action*100)<70?
                  'text-yellow-600':'text-green-600'}`}>
                    {(outputData?.scoring?.call_to_action
/inputData?.scoring_criteria?.call_to_action*100).toFixed(1)}

                  </span>
              </div>
              <span className="text-sm text-white mt-2">Call To Action</span>
            </div>
            <div className="flex flex-col items-center">
              <div 
              onClick={()=>handleVisible("audience_relevance")}
              className={`${(outputData?.scoring?.audience_relevance/inputData?.scoring_criteria?.audience_relevance*100)<30?'bg-red-100':
                (outputData?.scoring?.audience_relevance/inputData?.scoring_criteria?.audience_relevance*100)<70?
                'bg-yellow-100':'bg-green-100'}
              w-12 h-12 bg-green-100 rounded-full flex items-center justify-center`}>
                <span className={`${(outputData?.scoring?.audience_relevance/inputData?.scoring_criteria?.audience_relevance*100)<30?'text-red-600':
                  (outputData?.scoring?.audience_relevance/inputData?.scoring_criteria?.audience_relevance*100)<70?
                  'text-yellow-600':'text-green-600'}`}>{(outputData?.scoring?.audience_relevance
/inputData?.scoring_criteria?.audience_relevance*100).toFixed(1)}</span>
              </div>
              <span className="text-sm text-white mt-2">Audience Relevance</span>
            </div>
            <div className="flex flex-col items-center">
              <div 
              onClick={()=>handleVisible("brand_guideline_adherence")}
              className={`${(outputData?.scoring?.brand_guideline_adherence/inputData?.scoring_criteria?.brand_guideline_adherence*100)<30?'bg-red-100':
                (outputData?.scoring?.brand_guideline_adherence/inputData?.scoring_criteria?.brand_guideline_adherence*100)<70?
                'bg-yellow-100':'bg-green-100'} w-12 h-12 bg-green-100 rounded-full flex items-center justify-center`}>
                <span className={`${(outputData?.scoring?.brand_guideline_adherence/inputData?.scoring_criteria?.brand_guideline_adherence*100)<30?'text-red-600':
                  (outputData?.scoring?.brand_guideline_adherence/inputData?.scoring_criteria?.brand_guideline_adherence*100)<70?
                  'text-yellow-600':'text-green-600'}`}>{(outputData?.scoring?.brand_guideline_adherence
/inputData?.scoring_criteria?.brand_guideline_adherence*100).toFixed(1)}</span>
              </div>
              <span className="text-sm text-white mt-2">Brand Adherence</span>
            </div>
            <div className="flex flex-col items-center">
              <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center">
                <span className="text-green-600">{outputData?.scoring?.total_score}</span>
              </div>
              <span className="text-sm text-white mt-2">Total Score</span>
            </div>
          </div>
        </div>
      </div>
      {visible && (
        <div 
        onClick={()=>setVisible(false)}
        className='absolute inset-0 flex justify-center bg-opacity-0 items-center bg-transparent backdrop-blur-sm backdrop-filter p-4 w-screen h-screen rounded-md shadow-md'>
        <div className=' bg-white backdrop-blur-lg bg-opacity-5 backdrop-filter border-2 border-gray-900 rounded-2xl shadow-lg p-6 w-1/2 h-1/2'> 
        <div className='bg-gray-800 w-full h-full rounded-lg px-4 p-2'>
        <p className='text-xl text-white'>{outputData?.scoring?.justifications[key]}</p>
        </div>
        </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;

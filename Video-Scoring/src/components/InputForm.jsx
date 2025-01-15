import React from 'react'
import { useState } from 'react'
import { useSharedContext } from '../sharedContext'
import { Link } from 'react-router-dom';
import PropTypes from 'prop-types';
import Navbar from './Navbar';
import { FaUpload } from "react-icons/fa"; 
import axios from 'axios';


const InputForm = () => {

    InputForm.propTypes = {
        showForm: PropTypes.bool.isRequired,
        setShowForm: PropTypes.func.isRequired,
      };
      const [additional_guidelines,setAdditional]= useState('none')
      const [selected,setSelected] = useState([{id:0, selected:false},
        {id:1, selected:false},
        {id:2, selected:false},
        {id:3, selected:false},
        {id:4, selected:false},
        {id:5, selected:false}
      ])
      const [email,setEmail] = useState('')
      const [notification,setNotification] = useState(true)
      const [video_styles,setVideoStyles]= useState('')
      const {outputData,updateInputData,updateOutputData } = useSharedContext();
      const [product, setProduct] = useState('')
      const [tagline,setTagline] = useState('')
      const [brandPallete,setBrandPallete] = useState([{id:1,value:'#000000',colorName:'Black'}])
      const [height, setHeight] = useState(1080)
      const [width,setWidth] = useState(1920)
      const [CTA,setCTA] = useState('')
      const [Logo, setLogo] = useState('')
      const [Video, setVideo] = useState('')
      const [Duration, setDuration] = useState(5)
      const [showNav, setShowNav] = useState(true);
      const [scoringCriteria, setScoringCriteria] = useState([{
        id:0, criteria:'Background Foreground Separation', score:20,
      },{ id:1, criteria:'Brand Guideline Adherence', score:20,}
   ,{ id:2, criteria:"Creativity Visual Appeal",score:20,}
    ,{ id:3, criteria:"Product Focus",score:15,},
    { id:4, criteria:"Call To Action",score:15,}
    ,{ id:5, criteria:"Audience relevance",score:10,}])
    
      let lastScrollY = 1;

      const CLOUDINARY_URL_IMAGE = "https://api.cloudinary.com/v1_1/dzz1r3hcf/image/upload"
      const CLOUDINARY_URL_VIDEO = "https://api.cloudinary.com/v1_1/dzz1r3hcf/video/upload"
      const CLOUDINARY_UPLOAD_PRESET = "Logos_Videos"

      
      addEventListener("scroll", () => {
        if (window.scrollY < lastScrollY) {
          lastScrollY = window.scrollY;
          setShowNav(true);}
        else{
          setShowNav(false);
        }
       
        });
  
      const  handleCriteriaDelete= ()=>{
          setScoringCriteria(scoringCriteria.slice(0,scoringCriteria.length-1))
        } 

      function handleCriteriaAdd(){
          setScoringCriteria([...scoringCriteria,{id:scoringCriteria.length,Critera:'', score:0}])
          console.log(scoringCriteria)
        }  

      function handleAdd(){
        setBrandPallete([...brandPallete,{id:brandPallete.length+1,value:'#00000',colorName:'Black'}])
      }  
      const  handleDelete= ()=>{
        setBrandPallete(brandPallete.slice(0,brandPallete.length-1))
      } 

      async function scoreVideo(videoDetails, scoringCriteria) {
      const url = 'https://kanishak-video-scoring-api.hf.space/score-video';  
    
      
      const requestBody = {
        video_details: videoDetails,
        scoring_criteria: scoringCriteria,
        "additional_guidelines": additional_guidelines,
         "video_style":video_styles,
         "email": email
      };
    
      if(!requestBody){
        alert("request failed, Please Try Again!")
        updateOutputData({isSucessful: false});
      }
      
      updateOutputData({isSucessful: true});
      updateInputData(requestBody)  
      console.log('Request Body:', requestBody);
      console.log(outputData)
    
      try {
        const response = await fetch(url, {
          method: 'POST',  
          headers: {
            'Content-Type': 'application/json',  
          },
          body: JSON.stringify(requestBody), 
        });
    
        if (!response.ok) {
          updateOutputData({isSucessful: false});
          alert("request failed, Please Try Again!")
          throw new Error(`Error: ${response.statusText}`);
        }
    
        const data = await response.json();
        console.log('Scoring Result:', data);
        updateOutputData(data)
        console.log('Output Data:', outputData);
      } catch (error) {
        updateOutputData({isSucessful: false});
        alert("request failed, Please Try Again!")
        console.error('Request failed:', error);
      }
    }

    function Submit(){

      const valuesArray = brandPallete.map((item) => item.value);
      
      const videoDetails = {
            "product_name": product,
            "tagline": tagline,
            "brand_palette": valuesArray,
            "dimensions": {
              "width": width,
              "height": height
            },
            "duration": Duration,
            "cta_text": CTA,
            "logo_url": Logo,
            "product_video_url": Video
          }
    
          console.log("Before transformation:", scoringCriteria);
          const scoringCriteriaObject = scoringCriteria.reduce((acc, item) => {
            const key = item.criteria.toLowerCase().replace(/\s+/g, "_");
            acc[key] = item.score;
            return acc;
          }, {});

          scoreVideo(videoDetails, scoringCriteriaObject)
        
      }

      const handleCriteriaChange = (id, value) => {
        setScoringCriteria(
          scoringCriteria.map((field) => (field.id === id ? { ...field, criteria: value } : field))
        );
        console.log(scoringCriteria)
      }

      const handleScoreChange = (id, value) => {
        setScoringCriteria(
          scoringCriteria.map((field) => (field.id === id && parseInt(value) ? { ...field, score: parseInt(value) }: field))
        );
        console.log(scoringCriteria)
      }

      const handleInputChange = async(id,value)=>{
        const response = await fetch(`https://www.thecolorapi.com/id?hex=${value.slice(1)}`)
      const data = await response.json()
      const newcolorName = data.name.value
        setBrandPallete(
          brandPallete.map((field) => (field.id === id+1 ? { ...field, value: value, colorName:newcolorName } : field))
        );
        console.log(brandPallete)
      }

      const handleUploadImage = async (e) => {

        if (!e.target.files[0].type.startsWith("image/")) {
          alert("Please upload a valid image file!");
          return;
      }
        
        if (!e.target.files[0]) return;
        
        console.log('Uploading file:', e.target.files[0]);
        const formData = new FormData();
        formData.append('file', e.target.files[0]);
        formData.append('upload_preset', CLOUDINARY_UPLOAD_PRESET);
    
        try {
          const response = await axios.post(CLOUDINARY_URL_IMAGE, formData);
          const img = new Image();
          img.src = response.data.secure_url;
          img.onload = async () => {
            const { width, height } = img;
            const boundingBox = {
              x_min: 0,
              y_min: 0,
              x_max: width,
              y_max: height,
            };
            console.log('Bounding Box:', boundingBox);
            const Background_removed = await axios.post('https://kanishak-bgremove.hf.space/remove-background', {
              "image_url": response.data.secure_url,
              "bounding_box": boundingBox
            })
            console.log('Background Removed:', Background_removed.data.processed_image_url);
            setLogo(Background_removed.data.processed_image_url)
          }
        } catch (error) {
          console.error("Error uploading image:", error);
        }
      }

      const handleUploadVideo = async (e) => {
        
        if (!e.target.files[0]) return;
        
        console.log('Uploading file:', e.target.files[0]);
        const formData = new FormData();
        formData.append('file', e.target.files[0]);
        formData.append('upload_preset', CLOUDINARY_UPLOAD_PRESET);
    
        try {
          const response = await axios.post(CLOUDINARY_URL_VIDEO, formData);
          setVideo(response.data.secure_url)
          console.log('Uploaded URL:', response.data.secure_url);
        } catch (error) {
          console.error("Error uploading image:", error);
        }
      }

      const handleURLImageUpload = async (e) => {
        const img = new Image();
        img.src = e.target.value;
          img.onload = async () => {
            const { width, height } = img;
            const boundingBox = {
              x_min: 0,
              y_min: 0,
              x_max: width,
              y_max: height,
            };
            console.log('Bounding Box:', boundingBox);
            const Background_removed = await axios.post('https://kanishak-bgremove.hf.space/remove-background', {
              "image_url": e.target.value,
              "bounding_box": boundingBox
            })
            console.log('Background Removed:', Background_removed.data.processed_image_url);
            setLogo(Background_removed.data.processed_image_url)
          }
      }

        const artStyles = [{
          text:"Hand Drawn",
          background:'HandDrawn.png'
        },
        {
          text:"Handmade 3D",
          background:'Handmade3dBG.png'
        },
          { text:"Realistic Urban Drama",
            background:'relaisticBG.png'
          },
          {
          text:"2D Art",
          background:'2dArtBG.png'
          },
          {text:"Pop Art",
          background:'popBG.png'
          },
          {
           text:"Digital Engraving",
           background:'DigitalEngravingBG.png'
          }
        ];

        const handleEmail = (value)=>{
          const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
          if(emailRegex.test(value))
          notification? setEmail(value):setEmail('')
          else
          setEmail('')
        console.log(email)
        }

  return (
    <>
    <Navbar showNav={showNav} setShowForm={setShowNav} />
    <div className='bg-black bg-cover text-center pt-20 w-full h-full '>
      <div className=' flex justify-between items-center'>
      <h1 className='text-3xl my-5 mt-10 ml-24 text-white'>Fill In Your Video Details</h1>
      <Link to={`/dashboard/ `}>
      <button
      onClick={()=>Submit()} 
          className="px-5 py-2 border border-gray-400 mt-6 bg-gradient-to-r mr-28 to-[#6f36ac] from-[#7263b0] text-gray-200 font-bold rounded-lg shadow-lg hover:shadow-purple-500/65 transition"
        >

          Generate
        </button>
        </Link>
        </div>
        <div className='flex justify-evenly items-baseline'>
      <div className='flex flex-col gap-6 w-[65%] justify-start items-center'>
        <div className='flex gap-4 w-[100%] justify-evenly items-baseline'>

          <div className='flex flex-col gap-6 p-4 border-2 rounded-xl border-gray-500 justify-center items-baseline'>
          <h1 className='text-xl text-white'>Product Details</h1>
          <div className='flex flex-col gap-2 text-start'>
          <label className='text-white'>Product Name</label>
            <input type='text' 
            placeholder='Enter Product Name'
            className= 'inputbox' onChange={(e) => setProduct(e.target.value)} />
            </div>
            <div className='flex flex-col gap-2 text-start'>
          <label className='text-white'>Product Tagline</label>
            <input type='text' 
            placeholder='Enter Product Tagline'
            className=' inputbox' onChange={(e) => setTagline(e.target.value)} />
            </div>
            <div className='flex flex-col gap-2 text-start'>
              <div className='flex justify-start items-center gap-2'>
          <label className='text-white'>Brand Pallete</label>
          <button 
          onClick={handleAdd}
          className='w-6 h-6 flex justify-center items-center text-center bg-gradient-to-r from-[#ee9ca7] to-[#ffdde1] p-2 rounded-full bg-clip-text border-2 border-gray-400 '><p className='text-transparent text-2xl'>+</p></button>
           <button 
          onClick={()=>{handleDelete()}}
          className='w-6 h-6 flex justify-center items-center text-base bg-gradient-to-r from-[#ee9ca7] to-[#ffdde1] p-2 rounded-full border-2 border-gray-400 bg-clip-text '><p className='text-transparent text-2xl'>-</p></button>
          </div>
          <div className={`grid ${brandPallete.length<2?'grid-cols-1':'grid-cols-2'}  ${brandPallete.length<=2?'grid-rows-1':'grid-rows-2'} gap-2`}>
          {brandPallete.map((brand,index)=>(<div key ={index} className='flex justify-center items-center gap-2'>
          <div className={`${brandPallete.length<2?'w-60':'w-28'} bg-transparent flex items-center justify-between rounded-lg border border-[#fff] text-white p-2 h-8`}>
          <p className={`${brandPallete.length<2?'text-md':'text-xs'} truncate`}>{brand.colorName}</p>
          <div className={` w-5 h-5 rounded-full relative overflow-hidden border-2 border-zinc-400 gap-2`}>
            <input type='color' id='colorPicker' className={`bg-[${brand?.value}] outline-none border-none h-[180%] w-[180%] absolute top-0 left-0 translate-x-[-30%] translate-y-[-30%] rounded-full`} 
            onChange={(e)=>{
              handleInputChange(index,e.target.value)}} />
            </div>
            </div>
            </div>)
)}          </div>
            </div>
            </div>
            <div className='flex flex-col rounded-xl gap-6 p-4 border-2 border-gray-500 justify-center items-baseline'>
              <h1 className='text-xl text-white'>Video Dimensions</h1>
              <div className='flex flex-col gap-2 outline-none text-start'>
          <label className='text-white'>Video Width</label>
          <select
          id="width"
          value={width+'px'}
          onChange={(e)=>setWidth(parseInt(((e.target.value).slice(0,-2))))}
          className="border rounded-lg w-60 px-1 py-1 text-white bg-transparent"
        >
          <option
          className="bg-white text-black hover:bg-blue-100" value="320px">320px</option>
          <option  className="bg-white text-black hover:bg-blue-100" value="480px">480px</option>
          <option  className="bg-white text-black hover:bg-blue-100" value="1024px">1024px</option>
          <option  className="bg-white text-black hover:bg-blue-100" value="1080px">1080px</option>
          <option  className="bg-white text-black hover:bg-blue-100" value="1920px">1920px</option>
        </select>
            </div>
            <div className='flex flex-col gap-2 text-start'>
          <label className='text-white'>Video Height</label>
          <select
          id="height"
          value={height+'px'}
          onChange={(e) => setHeight(parseInt((e.target.value.slice(0,-2))))}
          className="border rounded-lg w-60 px-1 py-1 text-white bg-transparent"
        >
          <option  className="bg-white text-black hover:bg-blue-100" value="240px">240px</option>
          <option  className="bg-white text-black hover:bg-blue-100" value="480px">480px</option>
          <option  className="bg-white text-black hover:bg-blue-100" value="1024px">1024px</option>
          <option  className="bg-white text-black hover:bg-blue-100" value="1080px">1080px</option>
          <option  className="bg-white text-black hover:bg-blue-100" value="1920px">1920px</option>
        </select>
            </div>
            <div className='flex flex-col gap-2 text-start'>
          <label className='text-white'>Duration</label>
          <select
          id="height"
          value={Duration+'sec'}
          onChange={(e) => setDuration(parseInt((e.target.value.slice(0,-3))))}
          className="border rounded-lg w-60 px-1 py-1 text-white bg-transparent"
        >
          <option  className="bg-white text-black hover:bg-blue-100" value="5sec">5 sec</option>
          <option  className="bg-white text-black hover:bg-blue-100" value="10sec">10 sec</option>
          <option  className="bg-white text-black hover:bg-blue-100" value="15sec">15 sec</option>
          <option  className="bg-white text-black hover:bg-blue-100" value="20sec">20 sec</option>
          <option  className="bg-white text-black hover:bg-blue-100" value="25sec">25 sec</option>
          <option  className="bg-white text-black hover:bg-blue-100" value="30sec">30 sec</option>
        </select>
            </div>
            </div>
            <div className='flex flex-col gap-6 p-4 rounded-xl border-2 border-gray-500 justify-center items-baseline'>
            <h1 className='text-xl text-white'>Video Refference</h1>
            <div className='flex flex-col gap-2 text-start'>
          <label className='text-white'>Logo Url</label>
          <div className='flex justify-between items-center gap-3'>
            <input type='text' placeholder='Enter Logo Url or Upload Logo' 
            value={Logo?Logo:null}
            className='inputbox' onChange={(e) => handleURLImageUpload(e)} />
            <label htmlFor="image" className="cursor-pointer">
        <FaUpload className="text-lg text-white" />
      </label>
            <input
            id='image'
        type="file"
        accept="image/*"
        onChange={handleUploadImage}
        className="filebox hidden"/>
        </div>
            </div>
            <div className='flex flex-col gap-2 text-start'>
          <label className='text-white'>Video Url</label>
          <div className='flex justify-between items-center gap-3'>
            <input type='text' placeholder='Enter Video Url or Upload Video' className='inputbox' value={Video} onChange={(e) => setVideo(e.target.value)} />
            <label htmlFor="video" className="cursor-pointer">
        <FaUpload className="text-lg text-white" />
      </label>
            <input
        id='video'
        type="file"
        accept="video/*"
        onChange={handleUploadVideo}
        className="filebox hidden"/>
        </div>
            </div>
            <div className='flex flex-col gap-2 text-start'>
          <label className='text-white'>Call-To-Action</label>
            <input 
            style={{width:'270px'}}
            type='text' placeholder='Enter CTA Text' className='inputbox' onChange={(e) => setCTA(e.target.value)} />
            </div>
            </div>
          </div>
          <div className='flex gap-9 justify-evenly w-[100%] pb-4 items-center'>
            <div className={`flex flex-col w-[95%] gap-4 p-4 rounded-xl border-2 border-gray-500 justify-center items-baseline`}>
            <div className='flex justify-center gap-2 items-center'>
            <h1 className='text-white text-xl'>Art Styles</h1>
            <p  className='text-gray-500 mt-1 text-sm'>(Optional)</p>
            </div>
            <div className="flex flex-wrap gap-[17.2px] bg-transparent px-2 text-center">
      {artStyles.map((style, index) => (
        <button
        onClick={()=>{setVideoStyles(style.text)
          setSelected(
          selected.map((field)=>(field.id===index?{...field,selected:true}:{...field,selected:false}
          ))
          )
        }}
          style={{backgroundImage:`url(${style.background})`,
          backgroundPosition:'center'
        }}
          key={index}
          className={`text-white w-[32%] border-2 ${selected[index].selected?'border-pink-300':'border-gray-400'} hover:bg-gray-700 py-2 px-4 rounded-lg shadow-md transition-all duration-300 transform hover:scale-105`}
        >
          <p className='text-white'>{style.text}</p>
        </button>
      ))}
    </div>
            <div className='flex justify-center gap-2 items-center'>
            <h1 className='text-white text-xl'>Additional Guidelines</h1>
            <p  className='text-gray-500 mt-1 text-sm'>(Optional)</p>
            </div>
            <textarea
            onChange = {(e)=>{setAdditional(e.target.value)}}
            placeholder='How do you want your video to look like?' 
            style={{width:'100%',height:'75px',
              
            }}
            className='p-2 text-start h-20 placeholder:text-lg placeholder:italic rounded-lg text-white inputbox bg-transparent border-1 border-white ' />
          </div>
           </div>
        </div>
        <div className='h-full flex flex-col gap-5 -ml-10  justify-center mr-10'>  
        <div className='flex flex-col gap-[24px] p-4 rounded-xl border-2 border-gray-500 justify-start items-baseline'>
          <div className='flex justify-between w-full'>
            <h1 className='text-xl text-center mt-1 text-white'>Scoring Criteria</h1>
            <div className='flex gap-4'>
            <button
            onClick={handleCriteriaAdd}
        className="bg-gradient-to-r from-[#ee9ca7] to-[#ffdde1] text-black px-4 py-[2px] rounded mb-4"
      >
        Add
      </button>
      <button
      onClick={handleCriteriaDelete}
        className="bg-gradient-to-r from-[#ee9ca7] to-[#ffdde1] text-black px-4 py-1 rounded mb-4"
      >
        Del
      </button>
      </div>
            </div>
            {scoringCriteria.map((criteria,index)=>(
            <div key={index} className='flex gap-4 justify-evenly w-full'>
            <input type='text' className='inputbox text-ellipsis' 
            placeholder='Enter Criteria'
            value={criteria.criteria==''?null:criteria.criteria} onChange={(e) => handleCriteriaChange(index,e.target.value)} />
            <input type='text'
            placeholder='Score' 
            value={criteria.score<1?null:criteria.score}
            className=' text-center border border-white rounded-lg bg-transparent text-white'
            style={{width:'70px',
              padding:'2px',
            }}  
            onChange={(e) => handleScoreChange(index,e.target.value)} />
            </div>))}
            </div>
            <div className='flex flex-col gap-[24px] p-4 rounded-xl border-2 border-gray-500 justify-start items-baseline'>
            <h1 className='text-xl text-center text-white'>Account Details</h1>
            <div className='flex w-full flex-col gap-2 text-start'>
          <label className='text-white '>Email Adress</label>
            <input type='email' 
            placeholder='Enter your email address'
            className= 'inputbox placeholder:italic'
            style={{width:'100%'}}
            onChange={(e) => handleEmail(e.target.value)} />
            </div>
            <div className="flex w-full justify-between items-center">
              <h1 className='text-white text-start text-md'>Do you want notification<br></br> upon video completion??</h1>
      <div className='flex gap-3'>
      <button
        onClick={()=>setNotification(true)}
        className={`bg-green-500 text-white px-4 py-1 ${notification? 'border-2 border-white':''} rounded-lg hover:bg-green-600 transition duration-300`}
      >
        Yes
      </button>
      <button
        onClick={()=>setNotification(false)}
        className={`bg-red-500 text-white px-4 py-1 ${!notification? 'border-2 border-white':''} rounded-lg hover:bg-red-600 transition duration-300`}
      >
        No
      </button>
      </div>
    </div>
            </div>
            </div> 
        </div>           
    </div>
    </>
  )
}

export default InputForm
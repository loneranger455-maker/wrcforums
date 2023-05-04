import React, { useState,useEffect } from "react";
import axios from "axios";
import { GetToken } from "../../../services/Localstorageservice";
import { useNavigate, useParams } from "react-router";
import Topbar from "../Topbar";
import Sidebar from "../Sidebar";

function Updatepost() {
    const {id}=useParams()
    const navigate=useNavigate()
    const {access}=GetToken()
   
      const [title, setTitle] = useState("");
      const [contentvalue, setContentvalue] = useState("");
      const [link, setLink] = useState("");
   
  

  const HandleSubmit=(e)=>{
    console.log("hello world")
    e.preventDefault()
    const formdata=new FormData(e.target)
    // formdata.append("title",title)
    // formdata.append("contentvalue",contentvalue)
    // formdata.append("link",link)
    

    axios.put(`http://127.0.0.1:8000/api/user/allposts/${id}/`,formdata,{headers:{
        "authorization":`Bearer ${access}`
      }}).then((response)=>{
      console.log(response)
      navigate('/dashboard/activities')
      }
      )
      .catch((err)=>console.log(err))

    
  }
 
  useEffect(()=>{
   

    axios.get(`http://127.0.0.1:8000/api/user/getpostdata/${id}/`,{headers:{
        "authorization":`Bearer ${access}`
      }}).then((response)=>{
      console.log(response)
      setTitle(response.data.title)
      setContentvalue(response.data.contentvalue)
      setLink(response.data.link)
    //   navigate('/dashboard/activities')
      }
      )
      .catch((err)=>console.log(err))

    },[])

  return (
    <div className='flex'>
        <Sidebar value=""/>
      <div className="w-4/5">
        <Topbar />
    <div className="ml-20 mt-8 h-max overflow-scroll" >
      <form class="w-full max-w-xl flex flex-col gap-6" onSubmit={HandleSubmit}>
       
        <div>
        <label for='title'  className='text-sm'>Enter the title</label>

        <input id='title' value={title}  onChange={(e)=>setTitle(e.target.value)} type='text' name="title" className='bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500' placeholder='enter the title here' required/>

        </div>
        <div>
        <label for='textarea' className='text-sm'>Enter the content</label>
        <textarea id="textarea" onChange={(e)=>setContentvalue(e.target.value)} value={contentvalue} name="contentvalue" className="h-[20rem] bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
 >      </textarea>
        </div>
        <div>
        <input type='text' onChange={(e)=>setLink(e.target.value)} value={link} name="link" className='bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500' placeholder='post a link(Optional)' optional/>

        </div>
        <div className='flex w-full justify-between'>
            <div className='w-[10rem] bg-[var(--secondarycolor)] flex justify-around border rounded p-2.5 border-gray-300'>
            <input id='discussion' type='radio' name='post_type' value="discussion"/ >
            <label for='discussion'>Discussion</label> 
            </div>
            <div className='w-[10rem] bg-[var(--secondarycolor)]  flex justify-around border rounded p-2.5 border-gray-300'>
            <input id='question' type='radio' name='post_type' value="question"/ >
            <label for='question'>Question</label> 
            </div>
            <div className='w-[10rem] bg-[var(--secondarycolor)]  flex justify-around border rounded p-2.5 border-gray-300'>
            <input id='notice' type='radio' name='post_type' value="notice"/ >
            <label for='notice'>Notice</label> 
            </div>
            
        </div>
        <div className='text-center'>
            <input type='submit' value='submit' className='bg-[var(--primarycolor)] p-2.5 px-3.5 rounded'/>
        </div>
      </form>
    </div>
    </div>
    </div>
    
  );
}

export default Updatepost;

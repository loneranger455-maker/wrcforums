import React from 'react'
import Sidebar from './Sidebar'
import Topbar from './Topbar'
import { useState,useEffect } from 'react'
import axios from 'axios'
import { GetToken } from '../../services/Localstorageservice'

function ProfileCard(){
  const {access}=GetToken()
  const [data,setData]=useState({})
  useEffect(()=>{

    
    axios.get('http://127.0.0.1:8000/api/user/getdetails/',{headers:{
      "authorization":`Bearer ${access}`
    }}).then((response)=>
    setData(response.data)
   
    )
    .catch((err)=>console.log(err))
},[])
  return(
    <div>
   <div class="md:grid grid-cols-4 grid-rows-2  bg-white gap-2 p-4 rounded-xl">
        <div class="md:col-span-1 h-80 shadow-xl ">
                <div class="flex w-full h-full relative">
                    <img src={require('../../assets/user-profile-icon.png')} class="w-44 h-44 m-auto" alt=""/>

                </div>
        </div>
        <div class="md:col-span-3 h-80 shadow-xl p-4 space-y-2 ">
                <div class="flex ">
                    <span
                        class="text-sm   font-bold uppercase border-2 rounded-l px-4 py-2 bg-gray-50 whitespace-no-wrap w-2/6">Username:</span>
                    <input 
                        class="px-4 border-l-0 cursor-default border-gray-300 focus:outline-none  rounded-md rounded-l-none shadow-sm -ml-1 w-4/6"
                        type="text" value={data.username}
                        disabled/>
                </div>
                <div class="flex ">
                    <span
                        class="text-s font-bold uppercase border-2 rounded-l px-4 py-2 bg-gray-50 whitespace-no-wrap w-2/6">Email:</span>
                    <input 
                        class="px-4 border-l-0 cursor-default border-gray-300 focus:outline-none  rounded-md rounded-l-none shadow-sm -ml-1 w-4/6"
                        type="text" value={data.email}  disabled/>
                </div>
                 <div class="flex ">
                    <span
                        class="text-sm font-bold uppercase border-2 rounded-l px-4 py-2 bg-gray-50 whitespace-no-wrap w-2/6">Total posts posted:</span>
                    <input 
                        class="px-4 border-l-0 cursor-default border-gray-300 focus:outline-none  rounded-md rounded-l-none shadow-sm -ml-1 w-4/6"
                        type="text" value={data.content_count}  disabled/>
                </div>
                 <div class="flex ">
                    <span
                        class="text-sm font-bold uppercase border-2 rounded-l px-4 py-2 bg-gray-50 whitespace-no-wrap w-2/6">Total comments commented:</span>
                    <input 
                        class="px-4 border-l-0 cursor-default border-gray-300 focus:outline-none  rounded-md rounded-l-none shadow-sm -ml-1 w-4/6"
                        type="text" value={data.comment_count}  disabled/>
                </div>
        </div>
        {/* <div class="md:col-span-3 h-48 shadow-xl p-4 space-y-2 hidden md:block">
            <h3 class="font-bold uppercase"> Profile Description</h3>
            <p class=""> 
                Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris eget laoreet diam, id luctus lectus. Ut consectetur nisl ipsum, et faucibus sem finibus vitae. Maecenas aliquam dolor at dignissim commodo. Etiam a aliquam tellus, et suscipit dolor. Proin auctor nisi velit, quis aliquet sapien viverra a. 
            </p>
        </div> */}
            
    </div>
</div>
  )
}

function Settings() {
  
  return (
    <div className='flex'>
    <Sidebar value="settings" />
    <div  className='w-4/5'>
    <Topbar/>
    <div className='w-full h-full justify-center align-middle'>
      <div className='m-[4rem]'>
<ProfileCard/>
      </div>

    </div>
    </div>
   
</div>
  )
}

export default Settings
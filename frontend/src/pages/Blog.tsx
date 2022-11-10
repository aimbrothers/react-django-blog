import React, { useEffect, useState } from 'react'
import axios from 'axios'
import { postModel } from '../models/postModel';


  type GetPosts = {
    data: postModel[];
  };

const Blog: React.FC = () => {

const [data, setData] = useState<any>([])

const fetchData = () => {
  axios.get('http://127.0.0.1:8000/api/posts/')
      .then((res) => {
          setData(res.data)
      })}

      useEffect(() => {
        fetchData()
      }, [])
    
console.log(data)
    return (
      <div>
        {data.map((item:any) =>
        <div key={item.id}>
          <h1>{item.title}</h1>
          <p>{item.content}</p>
        </div>
        )}
      </div>
    )
  

}

export default Blog
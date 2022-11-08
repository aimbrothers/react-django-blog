import React, { useState } from 'react'
import axios from 'axios'

type Posts = {
    id: number;
    title: string;
    content: string;
    author: string;
  };
  
  type GetPosts = {
    data: Posts[];
  };

const Blog: React.FC = () => {

const [data, setData] = useState<any>([])

axios.get('http://127.0.0.1:8000/api/posts/')
    .then((res) => {
        console.log(res)
    })

  return (
    <div>Blog</div>
  )
}

export default Blog
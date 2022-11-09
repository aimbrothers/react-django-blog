import React, { useState } from 'react'
import axios from 'axios'
import { postModel } from '../models/postModel';


  type GetPosts = {
    data: postModel[];
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
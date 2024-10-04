import axios from "axios"


export const uploadVideo = (file: File) => {
    const formData = new FormData();
    formData.append('file', file);

    for (let [key, value] of formData.entries()) {
        console.log(`${key}:`, value);  // This should log the file
      }
  
    return axios.post('http://127.0.0.1:5000/upload', formData, {
        onUploadProgress(progressEvent) {
            console.log(progressEvent)
        },
    })
}
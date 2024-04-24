import axios from "@/utils/http"

export function loginCheck(params:any){
  return axios({
    url: 'api/login',
    method: 'post',
    headers: {
      'Content-Type': 'application/json;charset=UTF-8'
    },
    data: params
  })
}

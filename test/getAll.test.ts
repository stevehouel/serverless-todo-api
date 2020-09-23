const AWS = require('aws-sdk');
AWS.config.update({region:'eu-west-1'});
const axios = require('axios');
import { aws4Interceptor } from 'aws4-axios';

const apiEndpoint = process.env.TODO_API_ENDPOINT;

test('get all todos', async () => {
  const credentials = new AWS.SharedIniFileCredentials();

  const interceptor = aws4Interceptor({
    region: 'eu-west-1',
    service: 'execute-api'
  }, {
    accessKeyId: credentials.accessKeyId,
    secretAccessKey: credentials.secretAccessKey
  });
  
  axios.interceptors.request.use(interceptor);

  // Retrieve all todos
  console.log('GET Address', apiEndpoint + '/todos');
  const getAllResponse = await axios.get(apiEndpoint + '/todos');
  console.log('Response', getAllResponse.data);

  expect(getAllResponse.status).toBe(200);
});
const AWS = require('aws-sdk');
AWS.config.update({region:'eu-west-1'});
const axios = require('axios');
import { aws4Interceptor } from 'aws4-axios';

const apiEndpoint = process.env.TODO_API_ENDPOINT;

test('create todo', async () => {
  const credentials = new AWS.SharedIniFileCredentials();

  const interceptor = aws4Interceptor({
    region: 'eu-west-1',
    service: 'execute-api'
  }, {
    accessKeyId: credentials.accessKeyId,
    secretAccessKey: credentials.secretAccessKey
  });
  
  axios.interceptors.request.use(interceptor);
  axios.interceptors.response.use((response: any) => {
    return response;
  }, (error: any) => {
    return error.response;
  });

  // Create a new TODO
  const todoCreateRequest = {
    title: 'Create a new todo',
    content: 'This is a test of a new todo',
  };
  console.log('POST Address', apiEndpoint + '/todos');
  const createResponse = await axios.post(apiEndpoint + '/todos', todoCreateRequest);
  console.log('Response', createResponse.data);

  expect(createResponse.status).toBe(200);

  // Retrieve the TODO
  console.log('GET Address', apiEndpoint + '/todos/' + createResponse.data);
  const getResponse = await axios.get(apiEndpoint + '/todos/' + createResponse.data);
  console.log('Response', getResponse.data);

  expect(getResponse.status).toBe(200);
  expect(getResponse.data.title).toBe(todoCreateRequest.title);
  expect(getResponse.data.content).toBe(todoCreateRequest.content);
});
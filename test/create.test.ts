const AWS = require('aws-sdk');
const axios = require('axios');
const apiEndpoint = process.env.TODO_API_ENDPOINT;
const userPoolId = process.env.TODO_USER_POOL;
const userPoolClientId = process.env.TODO_USER_POOL_CLIENT;

test('create todo', async () => {
  const cognito = new AWS.CognitoIdentityServiceProvider();
  // TODO: Generate random values
  const userName = 'test-username';
  const password = 'super-secret-password';

  // Create a temporary cognito user
  cognito.adminCreateUser({
    UserPoolId: userPoolId,
    Username: userName,
    MessageAction: 'SUPPRESS',
  });
  cognito.adminSetUserPassword({
    UserPoolId: userPoolId,
    Username: userName,
    Password: password,
    Permanent: true,
  });

  // Retrieve a JWT token
  const cognitoResponse = await cognito.adminInitiateAuth({
    UserPoolId: userPoolId,
    ClientId: userPoolClientId,
    AuthFlow: 'ADMIN_NO_SRP_AUTH',
    AuthParameters: {
      USERNAME: userName,
      PASSWORD: password,
    },
  }).promise();
  const jwtToken = cognitoResponse.AuthenticationResult.IdToken;

  // Create a new TODO
  const todoCreateRequest = {
    title: 'Create a new todo',
    content: 'This is a test of a new todo',
  };
  const createResponse = await axios.post(apiEndpoint + '/todos', todoCreateRequest, { headers: {
    Authorization: jwtToken,
  }});

  // Retrieve the TODO
  const getResponse = await axios.get(apiEndpoint + '/todos/' + createResponse.data, { headers: {
    Authorization: jwtToken,
  }});

  expect(getResponse.status).toBe(200);
  expect(getResponse.data.title).toBe(todoCreateRequest.title);
  expect(getResponse.data.content).toBe(todoCreateRequest.content);

  // Delete the temporary user
  cognito.adminDeleteUser({
    UserPoolId: userPoolId,
    Username: userName,
  });
});
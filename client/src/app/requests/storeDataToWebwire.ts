import facebookImage from '@/images/Facebook_iOS_2019_icon_padded.png';
import convertStaticImageToBase64 from '@/convertImageToBase64';

const storeDataToVerbwire = async (input: string) => {
  const form = new FormData();
  form.append('name', 'UserInput');
  form.append('description', 'User input data');
  form.append('data', JSON.stringify([{ message: input }]));

  // Convert the image to base64
  const base64Image = await convertStaticImageToBase64(facebookImage);
  console.log('base64Image ', base64Image);
  form.append('filePath', base64Image);

  const options = {
    method: 'POST',
    headers: {
      accept: 'application/json',
      'X-API-Key': 'sk_live_e4f9b78b-de91-4917-a808-d73f10686ece'
    },
    body: form
  };

  try {
    const response = await fetch('https://api.verbwire.com/v1/nft/store/metadataFromImage', options);
    const result = await response.json();
    console.log('Data stored successfully:', result);
  } catch (error) {
    console.error('Error storing data:', error);
  }
};

export default storeDataToVerbwire;

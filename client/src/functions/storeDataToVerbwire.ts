import { saveAs } from 'file-saver'
const saveUrlsToFile = (metadataUrl: string, ipfsUrl: string) => {
    const blob = new Blob([`Metadata URL: ${metadataUrl}\nIPFS URL: ${ipfsUrl}`], { type: 'text/plain' });
    saveAs(blob, 'urls.txt');
};

const storeDataToVerbwire = async (data: any, file: File | null) => {
    const form = new FormData();
    form.append('name', 'UserInput');
    form.append('description', 'User input data');
    form.append('data', JSON.stringify([{ message: data }]));
  
    if (file) {
      form.append('filePath', file);
    }
  
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

      if (result.ipfs_storage.ipfs_url && result.ipfs_storage.metadata_url) [
        saveUrlsToFile(result.ipfs_storage.metadata_url, result.ipfs_storage.ipfs_url)
      ]
    } catch (error) {
      console.error('Error storing data:', error);
    }
  };
  
  export default storeDataToVerbwire;
  
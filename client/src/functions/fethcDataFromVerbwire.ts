const fetchDataFromIPFS = async (url: string) => {
    try {
      const response = await fetch(url);
      const data = await response.json();
      console.log('Data retrieved from IPFS:', data);
      return data;
    } catch (error) {
      console.error('Error retrieving data from IPFS:', error);
      throw error;
    }
  };
  
export default fetchDataFromIPFS;  
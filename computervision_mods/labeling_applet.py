#An Applet to label images.
#Input: DataLoader Object's masterkeychain attribute.

def applet(data.masterkeychain):
  populated_dict = {}
  for b in data.masterkeychain:
      if b not in populated_dict.keys():
          
          try:
              response = requests.get(f'https://webcams.nyctmc.org/api/cameras/{b}/image')
              response.raise_for_status()  # Raises an HTTPError for bad responses (4xx and 5xx status codes)
  
              image = Image.open(BytesIO(response.content))
  
              plt.imshow(image)
              plt.axis('off')  
              plt.show()
              label1 = input("1:protected,2:magicpaint,3:sharrow,4:nolane,5:bridge (or type 'exit' to end): ")
  
              if label1 == 'exit':
                  break
  
              label2 = input("dir? towards cam: t, away: a")
  
              populated_dict[b] = [label1,label2]
              plt.clf()
  
          except requests.exceptions.RequestException as e:
              print(f"Error during the request: {e}")
              next
  
          except Exception as e:
              print(f"An unexpected error occurred: {e}")
              next


  return populated dict



#feed this two lists of conditions to filter the dictionary on the basis of the values

#first list ['1','2','3','4','5']
#second list ['t','b','a',0']
  
def trimdict(populated_dict,filt1,filt2):
  return {key: value for key, value in populated_dict.items() if value[0] in filt1 and value[1] in filt2 }

      
    

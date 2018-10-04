import struct
#Import MagicaVoxel .VOX files and MagicaVoxel .PNG Palette Files
#by @matesteinforth

def import_vox(path):
    #parse file
    solids = []
    material_ids = []
    with open(path, 'rb') as f:
        
        #check filetype
        bytes = f.read(4)
        file_id = struct.unpack(">4s",  bytes)
        # print (file_id[0])
        if file_id[0] == b'VOX ':
    
            #init material list
            matlist = [];
            #skip header
            f.seek(56)
            
            #read number of voxels, stuct.unpack parses binary data to variables
            bytes = f.read(4)
            numvoxels = struct.unpack('<I', bytes)
            
            #iterate through voxels
            for x in range(0, numvoxels[0]):
                
                #read voxels, ( each voxel : 1 byte x 4 : x, y, z, colorIndex ) x numVoxels
                bytes = f.read(4)
                voxel = struct.unpack('<bbbB', bytes)    
                # print voxel
                #generate Cube and set position, change to 'Oinstance' for instances
                x,y,z = voxel[1], voxel[2], voxel[0]
                solids.append((x,y,z))
                
                #update material list, generate new material only if it isn't in the list yet
                matid = voxel[3]
                if matid not in matlist:
                    matlist.append(matid)
                material_ids.append(matid)
        else:
            print('Not a .VOX file')
            return None
    # print "solids", solids, "mats", material_ids
    return solids, material_ids
            
# def importPalette(path):
#     orig = bitmaps.BaseBitmap()
#     if orig.InitWith(path)[0] != c4d.IMAGERESULT_OK:
#         gui.MessageDialog("Cannot load image \"" + path + "\".")
#         return
    
#     width, height = orig.GetSize()
    
#     if height != 1:
#         gui.MessageDialog("This is not a MagicaVoxel .PNG Palette")
#     else:
#         for x in range(0, width):
#             mat = doc.SearchMaterial(str(x+1))
#             if mat:
#                 color = orig.GetPixel(x, 0)
#                 mat[c4d.MATERIAL_COLOR_COLOR]=c4d.Vector(float(color[0])/255, float(color[1])/255, float(color[2])/255)

def main():

    #fileselector and execute main function
    myFile = "/home/isaac/Desktop/comp460/tiles/boxWithHall.vox"
    import_vox(myFile)

    #fileselector and execute main function    
    # myFile = c4d.storage.LoadDialog(title="Open MagicaVoxel .PNG Palette File...")
    # importPalette(myFile)
    
    #update scene

if __name__=='__main__':
    main()
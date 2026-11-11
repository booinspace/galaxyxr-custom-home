import json, struct, zlib, binascii, pathlib, sys
p=pathlib.Path(sys.argv[1]); d=p/'resources/snow/day'; t=p/'resources/snow/thumbnail'; d.mkdir(parents=True,exist_ok=True); t.mkdir(parents=True,exist_ok=True)
# A double-sided unlit cube surrounds the viewer.
vertices=[-50,-50,-50,50,-50,-50,50,50,-50,-50,50,-50,-50,-50,50,50,-50,50,50,50,50,-50,50,50]
indices=[0,1,2,0,2,3,4,6,5,4,7,6,0,4,5,0,5,1,3,2,6,3,6,7,0,3,7,0,7,4,1,5,6,1,6,2]
binary=struct.pack('<24f36H',*vertices,*indices)
g={'asset':{'version':'2.0'},'extensionsUsed':['KHR_materials_unlit'],'extensionsRequired':['KHR_materials_unlit'],'scene':0,'scenes':[{'nodes':[0]}],'nodes':[{'mesh':0}],'meshes':[{'primitives':[{'attributes':{'POSITION':0},'indices':1,'material':0}]}],'materials':[{'doubleSided':True,'pbrMetallicRoughness':{'baseColorFactor':[0,0,0,1]},'extensions':{'KHR_materials_unlit':{}}}],'buffers':[{'byteLength':len(binary)}],'bufferViews':[{'buffer':0,'byteOffset':0,'byteLength':96,'target':34962},{'buffer':0,'byteOffset':96,'byteLength':72,'target':34963}],'accessors':[{'bufferView':0,'componentType':5126,'count':8,'type':'VEC3','min':[-50,-50,-50],'max':[50,50,50]},{'bufferView':1,'componentType':5123,'count':36,'type':'SCALAR'}]}
j=json.dumps(g,separators=(',',':')).encode(); j+=b' '*((-len(j))%4); binary+=b'\0'*((-len(binary))%4)
(d/'black.glb').write_bytes(struct.pack('<4sII',b'glTF',2,12+8+len(j)+8+len(binary))+struct.pack('<I4s',len(j),b'JSON')+j+struct.pack('<I4s',len(binary),b'BIN\0')+binary)
def chunk(k,v): return struct.pack('>I',len(v))+k+v+struct.pack('>I',binascii.crc32(k+v)&0xffffffff)
png=b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',128,128,8,2,0,0,0))+chunk(b'IDAT',zlib.compress((b'\0'+b'\0'*384)*128))+chunk(b'IEND',b'')
(d/'black.png').write_bytes(png); (t/'snow_thumb.png').write_bytes(png)
(p/'environment_list.xml').write_text('''<?xml version="1.0" encoding="UTF-8"?>\n<information><environment><packageName>boo.puppy.blackhome</packageName><name>snow</name><displayName>Black Home</displayName><thumbnail>snow_thumb.png</thumbnail><themeSupport>true</themeSupport></environment></information>\n''')
(p/'resources/snow/environment_information_jxr.xml').write_text('''<?xml version="1.0" encoding="UTF-8"?>\n<information><themeSupport>true</themeSupport><environment><name>day</name><path>resources/snow/day</path><thumbnail>black.png</thumbnail><skybox>lighting.zip</skybox><model>black.glb</model></environment></information>\n''')


workspace/appx/MetroApp.exe:     file format pei-i386


Disassembly of section .text:

00413b00 <.text+0x12b00>:
  413b00:	d8 43 00             	fadd   DWORD PTR [ebx+0x0]
  413b03:	c7 87 90 00 00 00 e8 	mov    DWORD PTR [edi+0x90],0x43d7e8
  413b0a:	d7 43 00 
  413b0d:	c7 47 0c 84 d6 43 00 	mov    DWORD PTR [edi+0xc],0x43d684
  413b14:	c7 87 a8 00 00 00 9c 	mov    DWORD PTR [edi+0xa8],0x43d59c
  413b1b:	d5 43 00 
  413b1e:	c7 87 ac 00 00 00 64 	mov    DWORD PTR [edi+0xac],0x43d564
  413b25:	d5 43 00 
  413b28:	c7 47 08 38 d5 43 00 	mov    DWORD PTR [edi+0x8],0x43d538
  413b2f:	c7 47 04 e4 d4 43 00 	mov    DWORD PTR [edi+0x4],0x43d4e4
  413b36:	c7 87 bc 00 00 00 ac 	mov    DWORD PTR [edi+0xbc],0x43d4ac
  413b3d:	d4 43 00 
  413b40:	c7 87 c4 00 00 00 88 	mov    DWORD PTR [edi+0xc4],0x43d488
  413b47:	d4 43 00 
  413b4a:	c7 87 c8 00 00 00 70 	mov    DWORD PTR [edi+0xc8],0x43d470
  413b51:	d4 43 00 
  413b54:	c7 87 cc 00 00 00 54 	mov    DWORD PTR [edi+0xcc],0x43d454
  413b5b:	d4 43 00 
  413b5e:	c7 87 d4 00 00 00 00 	mov    DWORD PTR [edi+0xd4],0x0
  413b65:	00 00 00 
  413b68:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [ebp-0x4],0x0
  413b6f:	c7 87 d8 00 00 00 00 	mov    DWORD PTR [edi+0xd8],0x0
  413b76:	00 00 00 
  413b79:	c7 87 dc 00 00 00 00 	mov    DWORD PTR [edi+0xdc],0x0
  413b80:	00 00 00 
  413b83:	57                   	push   edi
  413b84:	8d 8f e0 00 00 00    	lea    ecx,[edi+0xe0]
  413b8a:	c6 45 fc 02          	mov    BYTE PTR [ebp-0x4],0x2
  413b8e:	e8 2d fe ff ff       	call   0x4139c0
  413b93:	8d 4f 04             	lea    ecx,[edi+0x4]
  413b96:	c6 45 fc 03          	mov    BYTE PTR [ebp-0x4],0x3
  413b9a:	e8 51 de fe ff       	call   0x4019f0
  413b9f:	57                   	push   edi
  413ba0:	e8 3b ec 00 00       	call   0x4227e0
  413ba5:	83 c4 04             	add    esp,0x4
  413ba8:	8b c7                	mov    eax,edi
  413baa:	8b 4d f4             	mov    ecx,DWORD PTR [ebp-0xc]
  413bad:	64 89 0d 00 00 00 00 	mov    DWORD PTR fs:0x0,ecx
  413bb4:	59                   	pop    ecx
  413bb5:	5f                   	pop    edi
  413bb6:	5e                   	pop    esi
  413bb7:	8b e5                	mov    esp,ebp
  413bb9:	5d                   	pop    ebp
  413bba:	c3                   	ret
  413bbb:	cc                   	int3
  413bbc:	cc                   	int3
  413bbd:	cc                   	int3
  413bbe:	cc                   	int3
  413bbf:	cc                   	int3
  413bc0:	55                   	push   ebp
  413bc1:	8b ec                	mov    ebp,esp
  413bc3:	6a ff                	push   0xffffffff
  413bc5:	68 e8 d8 42 00       	push   0x42d8e8
  413bca:	64 a1 00 00 00 00    	mov    eax,fs:0x0
  413bd0:	50                   	push   eax
  413bd1:	81 ec ec 00 00 00    	sub    esp,0xec
  413bd7:	a1 f4 c1 43 00       	mov    eax,ds:0x43c1f4
  413bdc:	33 c5                	xor    eax,ebp
  413bde:	89 45 f0             	mov    DWORD PTR [ebp-0x10],eax
  413be1:	53                   	push   ebx
  413be2:	56                   	push   esi
  413be3:	57                   	push   edi
  413be4:	50                   	push   eax
  413be5:	8d 45 f4             	lea    eax,[ebp-0xc]
  413be8:	64 a3 00 00 00 00    	mov    fs:0x0,eax
  413bee:	8b 5d 08             	mov    ebx,DWORD PTR [ebp+0x8]
  413bf1:	6a 00                	push   0x0
  413bf3:	89 5d d4             	mov    DWORD PTR [ebp-0x2c],ebx
  413bf6:	e8 75 89 00 00       	call   0x41c570
  413bfb:	83 c4 04             	add    esp,0x4
  413bfe:	85 c0                	test   eax,eax
  413c00:	74 19                	je     0x413c1b
  413c02:	8d 4d a8             	lea    ecx,[ebp-0x58]
  413c05:	51                   	push   ecx
  413c06:	50                   	push   eax
  413c07:	e8 6c 8f 01 00       	call   0x42cb78
  413c0c:	85 c0                	test   eax,eax
  413c0e:	79 06                	jns    0x413c16
  413c10:	50                   	push   eax
  413c11:	e8 ca fc ff ff       	call   0x4138e0
  413c16:	8b 75 a8             	mov    esi,DWORD PTR [ebp-0x58]
  413c19:	eb 02                	jmp    0x413c1d
  413c1b:	33 f6                	xor    esi,esi
  413c1d:	89 75 a0             	mov    DWORD PTR [ebp-0x60],esi
  413c20:	89 75 80             	mov    DWORD PTR [ebp-0x80],esi
  413c23:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [ebp-0x4],0x0
  413c2a:	c7 45 c0 00 00 00 00 	mov    DWORD PTR [ebp-0x40],0x0
  413c31:	8d 45 e8             	lea    eax,[ebp-0x18]
  413c34:	50                   	push   eax
  413c35:	8d 85 44 ff ff ff    	lea    eax,[ebp-0xbc]
  413c3b:	50                   	push   eax
  413c3c:	6a 04                	push   0x4
  413c3e:	68 1c 09 43 00       	push   0x43091c
  413c43:	c6 45 fc 01          	mov    BYTE PTR [ebp-0x4],0x1
  413c47:	e8 4a 8f 01 00       	call   0x42cb96
  413c4c:	85 c0                	test   eax,eax
  413c4e:	79 06                	jns    0x413c56
  413c50:	50                   	push   eax
  413c51:	e8 8a fc ff ff       	call   0x4138e0
  413c56:	ff 75 e8             	push   DWORD PTR [ebp-0x18]
  413c59:	ff 15 74 01 43 00    	call   DWORD PTR ds:0x430174
  413c5f:	89 45 dc             	mov    DWORD PTR [ebp-0x24],eax
  413c62:	c6 45 fc 02          	mov    BYTE PTR [ebp-0x4],0x2
  413c66:	85 db                	test   ebx,ebx
  413c68:	75 04                	jne    0x413c6e
  413c6a:	33 ff                	xor    edi,edi
  413c6c:	eb 10                	jmp    0x413c7e
  413c6e:	8b bb c0 00 00 00    	mov    edi,DWORD PTR [ebx+0xc0]
  413c74:	85 ff                	test   edi,edi
  413c76:	74 06                	je     0x413c7e
  413c78:	8b 07                	mov    eax,DWORD PTR [edi]
  413c7a:	57                   	push   edi
  413c7b:	ff 50 04             	call   DWORD PTR [eax+0x4]
  413c7e:	89 7d b0             	mov    DWORD PTR [ebp-0x50],edi
  413c81:	57                   	push   edi
  413c82:	c6 45 fc 03          	mov    BYTE PTR [ebp-0x4],0x3
  413c86:	e8 b5 9f ff ff       	call   0x40dc40
  413c8b:	83 c4 04             	add    esp,0x4
  413c8e:	89 45 c4             	mov    DWORD PTR [ebp-0x3c],eax
  413c91:	33 c9                	xor    ecx,ecx
  413c93:	c6 45 fc 04          	mov    BYTE PTR [ebp-0x4],0x4
  413c97:	89 4d e0             	mov    DWORD PTR [ebp-0x20],ecx
  413c9a:	89 4d d0             	mov    DWORD PTR [ebp-0x30],ecx
  413c9d:	85 c0                	test   eax,eax
  413c9f:	74 1e                	je     0x413cbf
  413ca1:	8b 08                	mov    ecx,DWORD PTR [eax]
  413ca3:	8d 55 d0             	lea    edx,[ebp-0x30]
  413ca6:	52                   	push   edx
  413ca7:	68 b8 09 43 00       	push   0x4309b8
  413cac:	50                   	push   eax
  413cad:	ff 11                	call   DWORD PTR [ecx]
  413caf:	85 c0                	test   eax,eax
  413cb1:	79 06                	jns    0x413cb9
  413cb3:	50                   	push   eax
  413cb4:	e8 27 fc ff ff       	call   0x4138e0
  413cb9:	8b 4d d0             	mov    ecx,DWORD PTR [ebp-0x30]
  413cbc:	89 4d e0             	mov    DWORD PTR [ebp-0x20],ecx
  413cbf:	89 4d b8             	mov    DWORD PTR [ebp-0x48],ecx
  413cc2:	c6 45 fc 05          	mov    BYTE PTR [ebp-0x4],0x5
  413cc6:	ff 75 dc             	push   DWORD PTR [ebp-0x24]
  413cc9:	51                   	push   ecx
  413cca:	e8 a1 08 00 00       	call   0x414570
  413ccf:	83 c4 08             	add    esp,0x8
  413cd2:	89 45 8c             	mov    DWORD PTR [ebp-0x74],eax
  413cd5:	50                   	push   eax
  413cd6:	6a 01                	push   0x1
  413cd8:	c6 45 fc 06          	mov    BYTE PTR [ebp-0x4],0x6
  413cdc:	ff 15 c4 01 43 00    	call   DWORD PTR ds:0x4301c4
  413ce2:	89 45 ec             	mov    DWORD PTR [ebp-0x14],eax
  413ce5:	8d 45 d8             	lea    eax,[ebp-0x28]
  413ce8:	50                   	push   eax
  413ce9:	8d 85 1c ff ff ff    	lea    eax,[ebp-0xe4]
  413cef:	50                   	push   eax
  413cf0:	6a 03                	push   0x3
  413cf2:	68 28 09 43 00       	push   0x430928
  413cf7:	c6 45 fc 07          	mov    BYTE PTR [ebp-0x4],0x7
  413cfb:	e8 96 8e 01 00       	call   0x42cb96
  413d00:	85 c0                	test   eax,eax
  413d02:	79 06                	jns    0x413d0a
  413d04:	50                   	push   eax
  413d05:	e8 d6 fb ff ff       	call   0x4138e0
  413d0a:	ff 75 d8             	push   DWORD PTR [ebp-0x28]
  413d0d:	ff 15 74 01 43 00    	call   DWORD PTR ds:0x430174
  413d13:	89 45 c8             	mov    DWORD PTR [ebp-0x38],eax
  413d16:	c6 45 fc 08          	mov    BYTE PTR [ebp-0x4],0x8
  413d1a:	85 db                	test   ebx,ebx
  413d1c:	75 07                	jne    0x413d25
  413d1e:	33 c9                	xor    ecx,ecx
  413d20:	89 4d 9c             	mov    DWORD PTR [ebp-0x64],ecx
  413d23:	eb 16                	jmp    0x413d3b
  413d25:	8b 8b c0 00 00 00    	mov    ecx,DWORD PTR [ebx+0xc0]
  413d2b:	89 4d 9c             	mov    DWORD PTR [ebp-0x64],ecx
  413d2e:	85 c9                	test   ecx,ecx
  413d30:	74 09                	je     0x413d3b
  413d32:	8b 01                	mov    eax,DWORD PTR [ecx]
  413d34:	51                   	push   ecx
  413d35:	ff 50 04             	call   DWORD PTR [eax+0x4]
  413d38:	8b 4d 9c             	mov    ecx,DWORD PTR [ebp-0x64]
  413d3b:	89 4d bc             	mov    DWORD PTR [ebp-0x44],ecx
  413d3e:	51                   	push   ecx
  413d3f:	c6 45 fc 09          	mov    BYTE PTR [ebp-0x4],0x9
  413d43:	e8 f8 9e ff ff       	call   0x40dc40
  413d48:	83 c4 04             	add    esp,0x4
  413d4b:	89 45 88             	mov    DWORD PTR [ebp-0x78],eax
  413d4e:	33 c9                	xor    ecx,ecx
  413d50:	c6 45 fc 0a          	mov    BYTE PTR [ebp-0x4],0xa
  413d54:	89 4d e4             	mov    DWORD PTR [ebp-0x1c],ecx
  413d57:	89 4d cc             	mov    DWORD PTR [ebp-0x34],ecx
  413d5a:	85 c0                	test   eax,eax
  413d5c:	74 1e                	je     0x413d7c
  413d5e:	8b 08                	mov    ecx,DWORD PTR [eax]
  413d60:	8d 55 cc             	lea    edx,[ebp-0x34]
  413d63:	52                   	push   edx
  413d64:	68 b8 09 43 00       	push   0x4309b8
  413d69:	50                   	push   eax
  413d6a:	ff 11                	call   DWORD PTR [ecx]
  413d6c:	85 c0                	test   eax,eax
  413d6e:	79 06                	jns    0x413d76
  413d70:	50                   	push   eax
  413d71:	e8 6a fb ff ff       	call   0x4138e0
  413d76:	8b 4d cc             	mov    ecx,DWORD PTR [ebp-0x34]
  413d79:	89 4d e4             	mov    DWORD PTR [ebp-0x1c],ecx
  413d7c:	89 4d b4             	mov    DWORD PTR [ebp-0x4c],ecx
  413d7f:	c6 45 fc 0b          	mov    BYTE PTR [ebp-0x4],0xb
  413d83:	ff 75 c8             	push   DWORD PTR [ebp-0x38]
  413d86:	51                   	push   ecx
  413d87:	e8 e4 07 00 00       	call   0x414570
  413d8c:	83 c4 08             	add    esp,0x8
  413d8f:	89 45 94             	mov    DWORD PTR [ebp-0x6c],eax
  413d92:	50                   	push   eax
  413d93:	6a 01                	push   0x1
  413d95:	c6 45 fc 0c          	mov    BYTE PTR [ebp-0x4],0xc
  413d99:	ff 15 c4 01 43 00    	call   DWORD PTR ds:0x4301c4
  413d9f:	89 45 90             	mov    DWORD PTR [ebp-0x70],eax
  413da2:	c6 45 fc 0d          	mov    BYTE PTR [ebp-0x4],0xd
  413da6:	ff 75 ec             	push   DWORD PTR [ebp-0x14]
  413da9:	8b d0                	mov    edx,eax
  413dab:	e8 00 07 00 00       	call   0x4144b0
  413db0:	8b c8                	mov    ecx,eax
  413db2:	83 c4 04             	add    esp,0x4
  413db5:	89 4d 84             	mov    DWORD PTR [ebp-0x7c],ecx
  413db8:	c6 45 fc 1b          	mov    BYTE PTR [ebp-0x4],0x1b
  413dbc:	85 c9                	test   ecx,ecx
  413dbe:	74 09                	je     0x413dc9
  413dc0:	8b 01                	mov    eax,DWORD PTR [ecx]
  413dc2:	51                   	push   ecx
  413dc3:	ff 50 04             	call   DWORD PTR [eax+0x4]
  413dc6:	8b 4d 84             	mov    ecx,DWORD PTR [ebp-0x7c]
  413dc9:	89 8d 70 ff ff ff    	mov    DWORD PTR [ebp-0x90],ecx
  413dcf:	c6 45 fc 1a          	mov    BYTE PTR [ebp-0x4],0x1a
  413dd3:	85 c9                	test   ecx,ecx
  413dd5:	74 06                	je     0x413ddd
  413dd7:	8b 01                	mov    eax,DWORD PTR [ecx]
  413dd9:	51                   	push   ecx
  413dda:	ff 50 08             	call   DWORD PTR [eax+0x8]
  413ddd:	ff 75 90             	push   DWORD PTR [ebp-0x70]
  413de0:	e8 8d 8d 01 00       	call   0x42cb72
  413de5:	c6 45 fc 18          	mov    BYTE PTR [ebp-0x4],0x18
  413de9:	8b 4d 94             	mov    ecx,DWORD PTR [ebp-0x6c]
  413dec:	85 c9                	test   ecx,ecx
  413dee:	74 06                	je     0x413df6
  413df0:	8b 01                	mov    eax,DWORD PTR [ecx]
  413df2:	51                   	push   ecx
  413df3:	ff 50 08             	call   DWORD PTR [eax+0x8]
  413df6:	c6 45 fc 17          	mov    BYTE PTR [ebp-0x4],0x17
  413dfa:	8b 4d e4             	mov    ecx,DWORD PTR [ebp-0x1c]
  413dfd:	85 c9                	test   ecx,ecx
  413dff:	74 06                	je     0x413e07
  413e01:	8b 01                	mov    eax,DWORD PTR [ecx]
  413e03:	51                   	push   ecx
  413e04:	ff 50 08             	call   DWORD PTR [eax+0x8]
  413e07:	c6 45 fc 16          	mov    BYTE PTR [ebp-0x4],0x16
  413e0b:	8b 4d 88             	mov    ecx,DWORD PTR [ebp-0x78]
  413e0e:	85 c9                	test   ecx,ecx
  413e10:	74 06                	je     0x413e18
  413e12:	8b 01                	mov    eax,DWORD PTR [ecx]
  413e14:	51                   	push   ecx
  413e15:	ff 50 08             	call   DWORD PTR [eax+0x8]
  413e18:	8b 4d 9c             	mov    ecx,DWORD PTR [ebp-0x64]
  413e1b:	c6 45 fc 15          	mov    BYTE PTR [ebp-0x4],0x15
  413e1f:	85 c9                	test   ecx,ecx
  413e21:	74 06                	je     0x413e29
  413e23:	8b 01                	mov    eax,DWORD PTR [ecx]
  413e25:	51                   	push   ecx
  413e26:	ff 50 08             	call   DWORD PTR [eax+0x8]
  413e29:	c6 45 fc 14          	mov    BYTE PTR [ebp-0x4],0x14
  413e2d:	8b 4d c8             	mov    ecx,DWORD PTR [ebp-0x38]
  413e30:	85 c9                	test   ecx,ecx
  413e32:	74 06                	je     0x413e3a
  413e34:	8b 01                	mov    eax,DWORD PTR [ecx]
  413e36:	51                   	push   ecx
  413e37:	ff 50 08             	call   DWORD PTR [eax+0x8]
  413e3a:	ff 75 ec             	push   DWORD PTR [ebp-0x14]
  413e3d:	e8 30 8d 01 00       	call   0x42cb72
  413e42:	c6 45 fc 12          	mov    BYTE PTR [ebp-0x4],0x12
  413e46:	8b 4d 8c             	mov    ecx,DWORD PTR [ebp-0x74]
  413e49:	85 c9                	test   ecx,ecx
  413e4b:	74 06                	je     0x413e53
  413e4d:	8b 01                	mov    eax,DWORD PTR [ecx]
  413e4f:	51                   	push   ecx
  413e50:	ff 50 08             	call   DWORD PTR [eax+0x8]
  413e53:	c6 45 fc 11          	mov    BYTE PTR [ebp-0x4],0x11
  413e57:	8b 4d e0             	mov    ecx,DWORD PTR [ebp-0x20]
  413e5a:	85 c9                	test   ecx,ecx
  413e5c:	74 06                	je     0x413e64
  413e5e:	8b 01                	mov    eax,DWORD PTR [ecx]
  413e60:	51                   	push   ecx
  413e61:	ff 50 08             	call   DWORD PTR [eax+0x8]
  413e64:	c6 45 fc 10          	mov    BYTE PTR [ebp-0x4],0x10
  413e68:	8b 4d c4             	mov    ecx,DWORD PTR [ebp-0x3c]
  413e6b:	85 c9                	test   ecx,ecx
  413e6d:	74 06                	je     0x413e75
  413e6f:	8b 01                	mov    eax,DWORD PTR [ecx]
  413e71:	51                   	push   ecx
  413e72:	ff 50 08             	call   DWORD PTR [eax+0x8]
  413e75:	c6 45 fc 0f          	mov    BYTE PTR [ebp-0x4],0xf
  413e79:	85 ff                	test   edi,edi
  413e7b:	74 06                	je     0x413e83
  413e7d:	8b 07                	mov    eax,DWORD PTR [edi]
  413e7f:	57                   	push   edi
  413e80:	ff 50 08             	call   DWORD PTR [eax+0x8]
  413e83:	c6 45 fc 00          	mov    BYTE PTR [ebp-0x4],0x0
  413e87:	8b 4d dc             	mov    ecx,DWORD PTR [ebp-0x24]
  413e8a:	85 c9                	test   ecx,ecx
  413e8c:	74 06                	je     0x413e94
  413e8e:	8b 01                	mov    eax,DWORD PTR [ecx]
  413e90:	51                   	push   ecx
  413e91:	ff 50 08             	call   DWORD PTR [eax+0x8]
  413e94:	c6 45 fc 1c          	mov    BYTE PTR [ebp-0x4],0x1c
  413e98:	8b 8b d8 00 00 00    	mov    ecx,DWORD PTR [ebx+0xd8]
  413e9e:	33 ff                	xor    edi,edi
  413ea0:	89 7d dc             	mov    DWORD PTR [ebp-0x24],edi
  413ea3:	85 c9                	test   ecx,ecx
  413ea5:	74 1b                	je     0x413ec2
  413ea7:	8b 01                	mov    eax,DWORD PTR [ecx]
  413ea9:	8d 55 dc             	lea    edx,[ebp-0x24]
  413eac:	52                   	push   edx
  413ead:	68 a8 09 43 00       	push   0x4309a8
  413eb2:	51                   	push   ecx
  413eb3:	ff 10                	call   DWORD PTR [eax]
  413eb5:	85 c0                	test   eax,eax
  413eb7:	79 06                	jns    0x413ebf
  413eb9:	50                   	push   eax
  413eba:	e8 21 fa ff ff       	call   0x4138e0
  413ebf:	8b 7d dc             	mov    edi,DWORD PTR [ebp-0x24]
  413ec2:	89 7d c0             	mov    DWORD PTR [ebp-0x40],edi
  413ec5:	57                   	push   edi
  413ec6:	c6 45 fc 1d          	mov    BYTE PTR [ebp-0x4],0x1d
  413eca:	e8 11 b6 ff ff       	call   0x40f4e0
  413ecf:	83 c4 04             	add    esp,0x4
  413ed2:	89 45 ec             	mov    DWORD PTR [ebp-0x14],eax
  413ed5:	8d 45 e8             	lea    eax,[ebp-0x18]
  413ed8:	50                   	push   eax
  413ed9:	8d 85 58 ff ff ff    	lea    eax,[ebp-0xa8]
  413edf:	50                   	push   eax
  413ee0:	6a 06                	push   0x6
  413ee2:	68 30 09 43 00       	push   0x430930
  413ee7:	c6 45 fc 1e          	mov    BYTE PTR [ebp-0x4],0x1e
  413eeb:	e8 a6 8c 01 00       	call   0x42cb96
  413ef0:	85 c0                	test   eax,eax
  413ef2:	79 06                	jns    0x413efa
  413ef4:	50                   	push   eax
  413ef5:	e8 e6 f9 ff ff       	call   0x4138e0
  413efa:	8d 45 e0             	lea    eax,[ebp-0x20]
  413efd:	50                   	push   eax
  413efe:	ff 75 e8             	push   DWORD PTR [ebp-0x18]
  413f01:	c7 45 e0 00 00 00 00 	mov    DWORD PTR [ebp-0x20],0x0
  413f08:	ff 75 ec             	push   DWORD PTR [ebp-0x14]
  413f0b:	e8 80 8c 01 00       	call   0x42cb90
  413f10:	83 7d e0 00          	cmp    DWORD PTR [ebp-0x20],0x0
  413f14:	ff 75 ec             	push   DWORD PTR [ebp-0x14]
  413f17:	0f 94 45 9b          	sete   BYTE PTR [ebp-0x65]
  413f1b:	e8 52 8c 01 00       	call   0x42cb72
  413f20:	c6 45 fc 1c          	mov    BYTE PTR [ebp-0x4],0x1c
  413f24:	85 ff                	test   edi,edi
  413f26:	74 06                	je     0x413f2e
  413f28:	8b 07                	mov    eax,DWORD PTR [edi]
  413f2a:	57                   	push   edi
  413f2b:	ff 50 08             	call   DWORD PTR [eax+0x8]
  413f2e:	80 7d 9b 00          	cmp    BYTE PTR [ebp-0x65],0x0
  413f32:	74 5b                	je     0x413f8f
  413f34:	8d 45 ac             	lea    eax,[ebp-0x54]
  413f37:	50                   	push   eax
  413f38:	8d 85 58 ff ff ff    	lea    eax,[ebp-0xa8]
  413f3e:	50                   	push   eax
  413f3f:	6a 08                	push   0x8
  413f41:	68 40 09 43 00       	push   0x430940
  413f46:	e8 4b 8c 01 00       	call   0x42cb96
  413f4b:	85 c0                	test   eax,eax
  413f4d:	79 06                	jns    0x413f55
  413f4f:	50                   	push   eax
  413f50:	e8 8b f9 ff ff       	call   0x4138e0
  413f55:	8b 7d ac             	mov    edi,DWORD PTR [ebp-0x54]
  413f58:	3b f7                	cmp    esi,edi
  413f5a:	0f 84 8a 00 00 00    	je     0x413fea
  413f60:	85 f6                	test   esi,esi
  413f62:	74 06                	je     0x413f6a
  413f64:	56                   	push   esi
  413f65:	e8 08 8c 01 00       	call   0x42cb72
  413f6a:	33 f6                	xor    esi,esi
  413f6c:	89 75 a0             	mov    DWORD PTR [ebp-0x60],esi
  413f6f:	89 75 80             	mov    DWORD PTR [ebp-0x80],esi
  413f72:	85 ff                	test   edi,edi
  413f74:	74 74                	je     0x413fea
  413f76:	8d 45 dc             	lea    eax,[ebp-0x24]
  413f79:	50                   	push   eax
  413f7a:	57                   	push   edi
  413f7b:	e8 f8 8b 01 00       	call   0x42cb78
  413f80:	85 c0                	test   eax,eax
  413f82:	79 06                	jns    0x413f8a
  413f84:	50                   	push   eax
  413f85:	e8 56 f9 ff ff       	call   0x4138e0
  413f8a:	8b 75 dc             	mov    esi,DWORD PTR [ebp-0x24]
  413f8d:	eb 55                	jmp    0x413fe4
  413f8f:	8d 45 a4             	lea    eax,[ebp-0x5c]
  413f92:	50                   	push   eax
  413f93:	8d 85 30 ff ff ff    	lea    eax,[ebp-0xd0]
  413f99:	50                   	push   eax
  413f9a:	6a 05                	push   0x5
  413f9c:	68 54 09 43 00       	push   0x430954
  413fa1:	e8 f0 8b 01 00       	call   0x42cb96
  413fa6:	85 c0                	test   eax,eax
  413fa8:	79 06                	jns    0x413fb0
  413faa:	50                   	push   eax
  413fab:	e8 30 f9 ff ff       	call   0x4138e0
  413fb0:	8b 7d a4             	mov    edi,DWORD PTR [ebp-0x5c]
  413fb3:	3b f7                	cmp    esi,edi
  413fb5:	74 33                	je     0x413fea
  413fb7:	85 f6                	test   esi,esi
  413fb9:	74 06                	je     0x413fc1
  413fbb:	56                   	push   esi
  413fbc:	e8 b1 8b 01 00       	call   0x42cb72
  413fc1:	33 c0                	xor    eax,eax
  413fc3:	89 45 a0             	mov    DWORD PTR [ebp-0x60],eax
  413fc6:	89 45 80             	mov    DWORD PTR [ebp-0x80],eax
  413fc9:	85 ff                	test   edi,edi
  413fcb:	74 1d                	je     0x413fea
  413fcd:	8d 45 e0             	lea    eax,[ebp-0x20]
  413fd0:	50                   	push   eax
  413fd1:	57                   	push   edi
  413fd2:	e8 a1 8b 01 00       	call   0x42cb78
  413fd7:	85 c0                	test   eax,eax
  413fd9:	79 06                	jns    0x413fe1
  413fdb:	50                   	push   eax
  413fdc:	e8 ff f8 ff ff       	call   0x4138e0
  413fe1:	8b 75 e0             	mov    esi,DWORD PTR [ebp-0x20]
  413fe4:	89 75 a0             	mov    DWORD PTR [ebp-0x60],esi
  413fe7:	89 75 80             	mov    DWORD PTR [ebp-0x80],esi
  413fea:	8b 8b d8 00 00 00    	mov    ecx,DWORD PTR [ebx+0xd8]
  413ff0:	33 ff                	xor    edi,edi
  413ff2:	89 7d ec             	mov    DWORD PTR [ebp-0x14],edi
  413ff5:	85 c9                	test   ecx,ecx
  413ff7:	74 1b                	je     0x414014
  413ff9:	8b 01                	mov    eax,DWORD PTR [ecx]
  413ffb:	8d 55 ec             	lea    edx,[ebp-0x14]
  413ffe:	52                   	push   edx
  413fff:	68 a8 09 43 00       	push   0x4309a8
  414004:	51                   	push   ecx
  414005:	ff 10                	call   DWORD PTR [eax]
  414007:	85 c0                	test   eax,eax
  414009:	79 06                	jns    0x414011
  41400b:	50                   	push   eax
  41400c:	e8 cf f8 ff ff       	call   0x4138e0
  414011:	8b 7d ec             	mov    edi,DWORD PTR [ebp-0x14]
  414014:	89 7d c0             	mov    DWORD PTR [ebp-0x40],edi
  414017:	57                   	push   edi
  414018:	c6 45 fc 1f          	mov    BYTE PTR [ebp-0x4],0x1f
  41401c:	e8 bf b4 ff ff       	call   0x40f4e0
  414021:	83 c4 04             	add    esp,0x4
  414024:	8b f0                	mov    esi,eax
  414026:	56                   	push   esi
  414027:	e8 52 8b 01 00       	call   0x42cb7e
  41402c:	56                   	push   esi
  41402d:	89 45 e8             	mov    DWORD PTR [ebp-0x18],eax
  414030:	e8 3d 8b 01 00       	call   0x42cb72
  414035:	c6 45 fc 1c          	mov    BYTE PTR [ebp-0x4],0x1c
  414039:	85 ff                	test   edi,edi
  41403b:	74 06                	je     0x414043
  41403d:	8b 0f                	mov    ecx,DWORD PTR [edi]
  41403f:	57                   	push   edi
  414040:	ff 51 08             	call   DWORD PTR [ecx+0x8]
  414043:	83 7d e8 00          	cmp    DWORD PTR [ebp-0x18],0x0
  414047:	0f 84 21 04 00 00    	je     0x41446e
  41404d:	c7 45 9c 00 00 00 00 	mov    DWORD PTR [ebp-0x64],0x0
  414054:	8b 8b d8 00 00 00    	mov    ecx,DWORD PTR [ebx+0xd8]
  41405a:	33 f6                	xor    esi,esi
  41405c:	89 75 ec             	mov    DWORD PTR [ebp-0x14],esi
  41405f:	85 c9                	test   ecx,ecx
  414061:	74 19                	je     0x41407c
  414063:	8b 01                	mov    eax,DWORD PTR [ecx]
  414065:	8d 55 ec             	lea    edx,[ebp-0x14]
  414068:	52                   	push   edx
  414069:	68 a8 09 43 00       	push   0x4309a8
  41406e:	51                   	push   ecx
  41406f:	ff 10                	call   DWORD PTR [eax]
  414071:	85 c0                	test   eax,eax
  414073:	0f 88 97 fb ff ff    	js     0x413c10
  414079:	8b 75 ec             	mov    esi,DWORD PTR [ebp-0x14]
  41407c:	89 75 e8             	mov    DWORD PTR [ebp-0x18],esi
  41407f:	c7 45 e4 00 00 00 00 	mov    DWORD PTR [ebp-0x1c],0x0
  414086:	8d 4d e4             	lea    ecx,[ebp-0x1c]
  414089:	c6 45 fc 21          	mov    BYTE PTR [ebp-0x4],0x21
  41408d:	8b 06                	mov    eax,DWORD PTR [esi]
  41408f:	51                   	push   ecx
  414090:	56                   	push   esi
  414091:	ff 50 18             	call   DWORD PTR [eax+0x18]
  414094:	85 c0                	test   eax,eax
  414096:	0f 88 74 fb ff ff    	js     0x413c10
  41409c:	8b 45 e4             	mov    eax,DWORD PTR [ebp-0x1c]
  41409f:	85 c0                	test   eax,eax
  4140a1:	74 1a                	je     0x4140bd
  4140a3:	8d 4d b4             	lea    ecx,[ebp-0x4c]
  4140a6:	51                   	push   ecx
  4140a7:	50                   	push   eax
  4140a8:	e8 cb 8a 01 00       	call   0x42cb78
  4140ad:	85 c0                	test   eax,eax
  4140af:	0f 88 5b fb ff ff    	js     0x413c10
  4140b5:	8b 7d b4             	mov    edi,DWORD PTR [ebp-0x4c]
  4140b8:	8b 45 e4             	mov    eax,DWORD PTR [ebp-0x1c]
  4140bb:	eb 02                	jmp    0x4140bf
  4140bd:	33 ff                	xor    edi,edi
  4140bf:	50                   	push   eax
  4140c0:	e8 ad 8a 01 00       	call   0x42cb72
  4140c5:	57                   	push   edi
  4140c6:	e8 b3 8a 01 00       	call   0x42cb7e
  4140cb:	39 45 9c             	cmp    DWORD PTR [ebp-0x64],eax
  4140ce:	57                   	push   edi
  4140cf:	0f 92 c3             	setb   bl
  4140d2:	e8 9b 8a 01 00       	call   0x42cb72
  4140d7:	c6 45 fc 1c          	mov    BYTE PTR [ebp-0x4],0x1c
  4140db:	8b 06                	mov    eax,DWORD PTR [esi]
  4140dd:	56                   	push   esi
  4140de:	ff 50 08             	call   DWORD PTR [eax+0x8]
  4140e1:	84 db                	test   bl,bl
  4140e3:	0f 84 37 03 00 00    	je     0x414420
  4140e9:	8b 5d d4             	mov    ebx,DWORD PTR [ebp-0x2c]
  4140ec:	33 c9                	xor    ecx,ecx
  4140ee:	8b 93 d8 00 00 00    	mov    edx,DWORD PTR [ebx+0xd8]
  4140f4:	89 4d e8             	mov    DWORD PTR [ebp-0x18],ecx
  4140f7:	89 4d ec             	mov    DWORD PTR [ebp-0x14],ecx
  4140fa:	85 d2                	test   edx,edx
  4140fc:	74 1c                	je     0x41411a
  4140fe:	8b 02                	mov    eax,DWORD PTR [edx]
  414100:	8d 4d ec             	lea    ecx,[ebp-0x14]
  414103:	51                   	push   ecx
  414104:	68 a8 09 43 00       	push   0x4309a8
  414109:	52                   	push   edx
  41410a:	ff 10                	call   DWORD PTR [eax]
  41410c:	85 c0                	test   eax,eax
  41410e:	0f 88 fc fa ff ff    	js     0x413c10
  414114:	8b 4d ec             	mov    ecx,DWORD PTR [ebp-0x14]
  414117:	89 4d e8             	mov    DWORD PTR [ebp-0x18],ecx
  41411a:	89 8d 6c ff ff ff    	mov    DWORD PTR [ebp-0x94],ecx
  414120:	c7 45 e4 00 00 00 00 	mov    DWORD PTR [ebp-0x1c],0x0
  414127:	8d 55 e4             	lea    edx,[ebp-0x1c]
  41412a:	c6 45 fc 23          	mov    BYTE PTR [ebp-0x4],0x23
  41412e:	8b 01                	mov    eax,DWORD PTR [ecx]
  414130:	52                   	push   edx
  414131:	51                   	push   ecx
  414132:	ff 50 18             	call   DWORD PTR [eax+0x18]
  414135:	85 c0                	test   eax,eax
  414137:	0f 88 d3 fa ff ff    	js     0x413c10
  41413d:	8b 45 e4             	mov    eax,DWORD PTR [ebp-0x1c]
  414140:	85 c0                	test   eax,eax
  414142:	74 1a                	je     0x41415e
  414144:	8d 4d bc             	lea    ecx,[ebp-0x44]
  414147:	51                   	push   ecx
  414148:	50                   	push   eax
  414149:	e8 2a 8a 01 00       	call   0x42cb78
  41414e:	85 c0                	test   eax,eax
  414150:	0f 88 ba fa ff ff    	js     0x413c10
  414156:	8b 7d bc             	mov    edi,DWORD PTR [ebp-0x44]
  414159:	8b 45 e4             	mov    eax,DWORD PTR [ebp-0x1c]
  41415c:	eb 02                	jmp    0x414160
  41415e:	33 ff                	xor    edi,edi
  414160:	50                   	push   eax
  414161:	89 7d d8             	mov    DWORD PTR [ebp-0x28],edi
  414164:	e8 09 8a 01 00       	call   0x42cb72
  414169:	89 bd 7c ff ff ff    	mov    DWORD PTR [ebp-0x84],edi
  41416f:	c6 45 fc 24          	mov    BYTE PTR [ebp-0x4],0x24
  414173:	8b 93 d8 00 00 00    	mov    edx,DWORD PTR [ebx+0xd8]
  414179:	33 c9                	xor    ecx,ecx
  41417b:	89 4d 90             	mov    DWORD PTR [ebp-0x70],ecx
  41417e:	89 4d c8             	mov    DWORD PTR [ebp-0x38],ecx
  414181:	85 d2                	test   edx,edx
  414183:	74 1c                	je     0x4141a1
  414185:	8b 02                	mov    eax,DWORD PTR [edx]
  414187:	8d 4d c8             	lea    ecx,[ebp-0x38]
  41418a:	51                   	push   ecx
  41418b:	68 a8 09 43 00       	push   0x4309a8
  414190:	52                   	push   edx
  414191:	ff 10                	call   DWORD PTR [eax]
  414193:	85 c0                	test   eax,eax
  414195:	0f 88 75 fa ff ff    	js     0x413c10
  41419b:	8b 4d c8             	mov    ecx,DWORD PTR [ebp-0x38]
  41419e:	89 4d 90             	mov    DWORD PTR [ebp-0x70],ecx
  4141a1:	89 8d 78 ff ff ff    	mov    DWORD PTR [ebp-0x88],ecx
  4141a7:	c7 45 cc 00 00 00 00 	mov    DWORD PTR [ebp-0x34],0x0
  4141ae:	8d 55 cc             	lea    edx,[ebp-0x34]
  4141b1:	c6 45 fc 26          	mov    BYTE PTR [ebp-0x4],0x26
  4141b5:	8b 01                	mov    eax,DWORD PTR [ecx]
  4141b7:	52                   	push   edx
  4141b8:	51                   	push   ecx
  4141b9:	ff 50 18             	call   DWORD PTR [eax+0x18]
  4141bc:	85 c0                	test   eax,eax
  4141be:	0f 88 4c fa ff ff    	js     0x413c10
  4141c4:	8b 45 cc             	mov    eax,DWORD PTR [ebp-0x34]
  4141c7:	85 c0                	test   eax,eax
  4141c9:	74 1a                	je     0x4141e5
  4141cb:	8d 4d b8             	lea    ecx,[ebp-0x48]
  4141ce:	51                   	push   ecx
  4141cf:	50                   	push   eax
  4141d0:	e8 a3 89 01 00       	call   0x42cb78
  4141d5:	85 c0                	test   eax,eax
  4141d7:	0f 88 33 fa ff ff    	js     0x413c10
  4141dd:	8b 75 b8             	mov    esi,DWORD PTR [ebp-0x48]
  4141e0:	8b 45 cc             	mov    eax,DWORD PTR [ebp-0x34]
  4141e3:	eb 02                	jmp    0x4141e7
  4141e5:	33 f6                	xor    esi,esi
  4141e7:	50                   	push   eax
  4141e8:	89 75 94             	mov    DWORD PTR [ebp-0x6c],esi
  4141eb:	e8 82 89 01 00       	call   0x42cb72
  4141f0:	89 b5 74 ff ff ff    	mov    DWORD PTR [ebp-0x8c],esi
  4141f6:	c6 45 fc 27          	mov    BYTE PTR [ebp-0x4],0x27
  4141fa:	8b 93 d8 00 00 00    	mov    edx,DWORD PTR [ebx+0xd8]
  414200:	33 c9                	xor    ecx,ecx
  414202:	89 4d 88             	mov    DWORD PTR [ebp-0x78],ecx
  414205:	89 4d c4             	mov    DWORD PTR [ebp-0x3c],ecx
  414208:	85 d2                	test   edx,edx
  41420a:	74 1c                	je     0x414228
  41420c:	8b 02                	mov    eax,DWORD PTR [edx]
  41420e:	8d 4d c4             	lea    ecx,[ebp-0x3c]
  414211:	51                   	push   ecx
  414212:	68 a8 09 43 00       	push   0x4309a8
  414217:	52                   	push   edx
  414218:	ff 10                	call   DWORD PTR [eax]
  41421a:	85 c0                	test   eax,eax
  41421c:	0f 88 ee f9 ff ff    	js     0x413c10
  414222:	8b 4d c4             	mov    ecx,DWORD PTR [ebp-0x3c]
  414225:	89 4d 88             	mov    DWORD PTR [ebp-0x78],ecx
  414228:	89 4d 8c             	mov    DWORD PTR [ebp-0x74],ecx
  41422b:	c7 45 d0 00 00 00 00 	mov    DWORD PTR [ebp-0x30],0x0
  414232:	8d 55 d0             	lea    edx,[ebp-0x30]
  414235:	c6 45 fc 29          	mov    BYTE PTR [ebp-0x4],0x29
  414239:	8b 01                	mov    eax,DWORD PTR [ecx]
  41423b:	52                   	push   edx
  41423c:	51                   	push   ecx
  41423d:	ff 50 18             	call   DWORD PTR [eax+0x18]
  414240:	85 c0                	test   eax,eax
  414242:	0f 88 c8 f9 ff ff    	js     0x413c10
  414248:	8b 45 d0             	mov    eax,DWORD PTR [ebp-0x30]
  41424b:	85 c0                	test   eax,eax
  41424d:	74 1a                	je     0x414269
  41424f:	8d 4d b0             	lea    ecx,[ebp-0x50]
  414252:	51                   	push   ecx
  414253:	50                   	push   eax
  414254:	e8 1f 89 01 00       	call   0x42cb78
  414259:	85 c0                	test   eax,eax
  41425b:	0f 88 af f9 ff ff    	js     0x413c10
  414261:	8b 5d b0             	mov    ebx,DWORD PTR [ebp-0x50]
  414264:	8b 45 d0             	mov    eax,DWORD PTR [ebp-0x30]
  414267:	eb 02                	jmp    0x41426b
  414269:	33 db                	xor    ebx,ebx
  41426b:	50                   	push   eax
  41426c:	89 5d 8c             	mov    DWORD PTR [ebp-0x74],ebx
  41426f:	e8 fe 88 01 00       	call   0x42cb72
  414274:	6a 00                	push   0x0
  414276:	57                   	push   edi
  414277:	e8 08 89 01 00       	call   0x42cb84
  41427c:	6a 00                	push   0x0
  41427e:	56                   	push   esi
  41427f:	8b f8                	mov    edi,eax
  414281:	e8 fe 88 01 00       	call   0x42cb84
  414286:	6a 00                	push   0x0
  414288:	53                   	push   ebx
  414289:	8b f0                	mov    esi,eax
  41428b:	e8 f4 88 01 00       	call   0x42cb84
  414290:	8b 5d 9c             	mov    ebx,DWORD PTR [ebp-0x64]
  414293:	ff 75 8c             	push   DWORD PTR [ebp-0x74]
  414296:	0f b7 0c 5e          	movzx  ecx,WORD PTR [esi+ebx*2]
  41429a:	8a 14 58             	mov    dl,BYTE PTR [eax+ebx*2]
  41429d:	83 e1 0f             	and    ecx,0xf
  4142a0:	83 e1 07             	and    ecx,0x7
  4142a3:	d2 c2                	rol    dl,cl
  4142a5:	8b c3                	mov    eax,ebx
  4142a7:	83 e0 07             	and    eax,0x7
  4142aa:	32 90 a8 07 43 00    	xor    dl,BYTE PTR [eax+0x4307a8]
  4142b0:	0f b6 c2             	movzx  eax,dl
  4142b3:	66 39 44 5f 02       	cmp    WORD PTR [edi+ebx*2+0x2],ax
  4142b8:	0f 95 c3             	setne  bl
  4142bb:	e8 b2 88 01 00       	call   0x42cb72
  4142c0:	c6 45 fc 27          	mov    BYTE PTR [ebp-0x4],0x27
  4142c4:	8b 4d 88             	mov    ecx,DWORD PTR [ebp-0x78]
  4142c7:	51                   	push   ecx
  4142c8:	8b 01                	mov    eax,DWORD PTR [ecx]
  4142ca:	ff 50 08             	call   DWORD PTR [eax+0x8]
  4142cd:	ff 75 94             	push   DWORD PTR [ebp-0x6c]
  4142d0:	e8 9d 88 01 00       	call   0x42cb72
  4142d5:	c6 45 fc 24          	mov    BYTE PTR [ebp-0x4],0x24
  4142d9:	8b 4d 90             	mov    ecx,DWORD PTR [ebp-0x70]
  4142dc:	51                   	push   ecx
  4142dd:	8b 01                	mov    eax,DWORD PTR [ecx]
  4142df:	ff 50 08             	call   DWORD PTR [eax+0x8]
  4142e2:	ff 75 d8             	push   DWORD PTR [ebp-0x28]
  4142e5:	e8 88 88 01 00       	call   0x42cb72
  4142ea:	c6 45 fc 1c          	mov    BYTE PTR [ebp-0x4],0x1c
  4142ee:	8b 4d e8             	mov    ecx,DWORD PTR [ebp-0x18]
  4142f1:	51                   	push   ecx
  4142f2:	8b 01                	mov    eax,DWORD PTR [ecx]
  4142f4:	ff 50 08             	call   DWORD PTR [eax+0x8]
  4142f7:	84 db                	test   bl,bl
  4142f9:	0f 84 16 01 00 00    	je     0x414415
  4142ff:	8d 45 c0             	lea    eax,[ebp-0x40]
  414302:	50                   	push   eax
  414303:	8d 85 08 ff ff ff    	lea    eax,[ebp-0xf8]
  414309:	50                   	push   eax
  41430a:	6a 03                	push   0x3
  41430c:	68 60 09 43 00       	push   0x430960
  414311:	e8 80 88 01 00       	call   0x42cb96
  414316:	85 c0                	test   eax,eax
  414318:	0f 88 f2 f8 ff ff    	js     0x413c10
  41431e:	ff 75 c0             	push   DWORD PTR [ebp-0x40]
  414321:	ff 15 74 01 43 00    	call   DWORD PTR ds:0x430174
  414327:	89 45 d8             	mov    DWORD PTR [ebp-0x28],eax
  41432a:	c6 45 fc 2a          	mov    BYTE PTR [ebp-0x4],0x2a
  41432e:	8b 75 d4             	mov    esi,DWORD PTR [ebp-0x2c]
  414331:	8b b6 c0 00 00 00    	mov    esi,DWORD PTR [esi+0xc0]
  414337:	85 f6                	test   esi,esi
  414339:	74 06                	je     0x414341
  41433b:	8b 0e                	mov    ecx,DWORD PTR [esi]
  41433d:	56                   	push   esi
  41433e:	ff 51 04             	call   DWORD PTR [ecx+0x4]
  414341:	89 b5 74 ff ff ff    	mov    DWORD PTR [ebp-0x8c],esi
  414347:	56                   	push   esi
  414348:	c6 45 fc 2b          	mov    BYTE PTR [ebp-0x4],0x2b
  41434c:	e8 ef 98 ff ff       	call   0x40dc40
  414351:	8b f8                	mov    edi,eax
  414353:	83 c4 04             	add    esp,0x4
  414356:	89 bd 78 ff ff ff    	mov    DWORD PTR [ebp-0x88],edi
  41435c:	33 db                	xor    ebx,ebx
  41435e:	c6 45 fc 2c          	mov    BYTE PTR [ebp-0x4],0x2c
  414362:	89 5d e8             	mov    DWORD PTR [ebp-0x18],ebx
  414365:	85 ff                	test   edi,edi
  414367:	74 19                	je     0x414382
  414369:	8b 0f                	mov    ecx,DWORD PTR [edi]
  41436b:	8d 45 e8             	lea    eax,[ebp-0x18]
  41436e:	50                   	push   eax
  41436f:	68 b8 09 43 00       	push   0x4309b8
  414374:	57                   	push   edi
  414375:	ff 11                	call   DWORD PTR [ecx]
  414377:	85 c0                	test   eax,eax
  414379:	0f 88 91 f8 ff ff    	js     0x413c10
  41437f:	8b 5d e8             	mov    ebx,DWORD PTR [ebp-0x18]
  414382:	89 9d 7c ff ff ff    	mov    DWORD PTR [ebp-0x84],ebx
  414388:	c6 45 fc 2d          	mov    BYTE PTR [ebp-0x4],0x2d
  41438c:	ff 75 d8             	push   DWORD PTR [ebp-0x28]
  41438f:	53                   	push   ebx
  414390:	e8 db 01 00 00       	call   0x414570
  414395:	83 c4 08             	add    esp,0x8
  414398:	89 45 94             	mov    DWORD PTR [ebp-0x6c],eax
  41439b:	50                   	push   eax
  41439c:	6a 01                	push   0x1
  41439e:	c6 45 fc 2e          	mov    BYTE PTR [ebp-0x4],0x2e
  4143a2:	ff 15 c4 01 43 00    	call   DWORD PTR ds:0x4301c4
  4143a8:	89 45 90             	mov    DWORD PTR [ebp-0x70],eax
  4143ab:	c6 45 fc 2f          	mov    BYTE PTR [ebp-0x4],0x2f
  4143af:	8b 55 84             	mov    edx,DWORD PTR [ebp-0x7c]
  4143b2:	50                   	push   eax
  4143b3:	8b 0a                	mov    ecx,DWORD PTR [edx]
  4143b5:	52                   	push   edx
  4143b6:	ff 51 38             	call   DWORD PTR [ecx+0x38]
  4143b9:	85 c0                	test   eax,eax
  4143bb:	0f 88 4f f8 ff ff    	js     0x413c10
  4143c1:	ff 75 90             	push   DWORD PTR [ebp-0x70]
  4143c4:	e8 a9 87 01 00       	call   0x42cb72
  4143c9:	c6 45 fc 2d          	mov    BYTE PTR [ebp-0x4],0x2d
  4143cd:	8b 4d 94             	mov    ecx,DWORD PTR [ebp-0x6c]
  4143d0:	85 c9                	test   ecx,ecx
  4143d2:	74 06                	je     0x4143da
  4143d4:	8b 01                	mov    eax,DWORD PTR [ecx]
  4143d6:	51                   	push   ecx
  4143d7:	ff 50 08             	call   DWORD PTR [eax+0x8]
  4143da:	c6 45 fc 2c          	mov    BYTE PTR [ebp-0x4],0x2c
  4143de:	85 db                	test   ebx,ebx
  4143e0:	74 06                	je     0x4143e8
  4143e2:	8b 03                	mov    eax,DWORD PTR [ebx]
  4143e4:	53                   	push   ebx
  4143e5:	ff 50 08             	call   DWORD PTR [eax+0x8]
  4143e8:	c6 45 fc 2b          	mov    BYTE PTR [ebp-0x4],0x2b
  4143ec:	85 ff                	test   edi,edi
  4143ee:	74 06                	je     0x4143f6
  4143f0:	8b 07                	mov    eax,DWORD PTR [edi]
  4143f2:	57                   	push   edi
  4143f3:	ff 50 08             	call   DWORD PTR [eax+0x8]
  4143f6:	c6 45 fc 2a          	mov    BYTE PTR [ebp-0x4],0x2a
  4143fa:	85 f6                	test   esi,esi
  4143fc:	74 06                	je     0x414404
  4143fe:	8b 06                	mov    eax,DWORD PTR [esi]
  414400:	56                   	push   esi
  414401:	ff 50 08             	call   DWORD PTR [eax+0x8]
  414404:	c6 45 fc 1c          	mov    BYTE PTR [ebp-0x4],0x1c
  414408:	8b 4d d8             	mov    ecx,DWORD PTR [ebp-0x28]
  41440b:	85 c9                	test   ecx,ecx
  41440d:	74 06                	je     0x414415
  41440f:	8b 01                	mov    eax,DWORD PTR [ecx]
  414411:	51                   	push   ecx
  414412:	ff 50 08             	call   DWORD PTR [eax+0x8]
  414415:	ff 45 9c             	inc    DWORD PTR [ebp-0x64]
  414418:	8b 5d d4             	mov    ebx,DWORD PTR [ebp-0x2c]
  41441b:	e9 34 fc ff ff       	jmp    0x414054
  414420:	c7 45 d4 00 00 00 00 	mov    DWORD PTR [ebp-0x2c],0x0
  414427:	c6 45 fc 30          	mov    BYTE PTR [ebp-0x4],0x30
  41442b:	8b 75 84             	mov    esi,DWORD PTR [ebp-0x7c]
  41442e:	8d 4d d4             	lea    ecx,[ebp-0x2c]
  414431:	8b 06                	mov    eax,DWORD PTR [esi]
  414433:	51                   	push   ecx
  414434:	56                   	push   esi
  414435:	ff 50 3c             	call   DWORD PTR [eax+0x3c]
  414438:	85 c0                	test   eax,eax
  41443a:	79 06                	jns    0x414442
  41443c:	50                   	push   eax
  41443d:	e8 9e f4 ff ff       	call   0x4138e0
  414442:	8b 4d d4             	mov    ecx,DWORD PTR [ebp-0x2c]
  414445:	8b f9                	mov    edi,ecx
  414447:	85 c9                	test   ecx,ecx
  414449:	74 09                	je     0x414454
  41444b:	8b 01                	mov    eax,DWORD PTR [ecx]
  41444d:	51                   	push   ecx
  41444e:	ff                   	.byte 0xff
  41444f:	50                   	push   eax


workspace/appx/MetroApp.exe:     file format pei-i386


Disassembly of section .text:

0042ca80 <.text+0x2ba80>:
  42ca80:	d4 4e                	aam    0x4e
  42ca82:	43                   	inc    ebx
  42ca83:	00 bf d4 4e 43 00    	add    BYTE PTR [edi+0x434ed4],bh
  42ca89:	eb 0b                	jmp    0x42ca96
  42ca8b:	8b 06                	mov    eax,DWORD PTR [esi]
  42ca8d:	85 c0                	test   eax,eax
  42ca8f:	74 02                	je     0x42ca93
  42ca91:	ff d0                	call   eax
  42ca93:	83 c6 04             	add    esi,0x4
  42ca96:	3b f7                	cmp    esi,edi
  42ca98:	72 f1                	jb     0x42ca8b
  42ca9a:	5f                   	pop    edi
  42ca9b:	5e                   	pop    esi
  42ca9c:	c3                   	ret
  42ca9d:	cc                   	int3
  42ca9e:	ff 25 7c 00 43 00    	jmp    DWORD PTR ds:0x43007c
  42caa4:	ff 25 80 00 43 00    	jmp    DWORD PTR ds:0x430080
  42caaa:	68 00 00 44 00       	push   0x440000
  42caaf:	e8 a0 00 00 00       	call   0x42cb54
  42cab4:	59                   	pop    ecx
  42cab5:	c3                   	ret
  42cab6:	55                   	push   ebp
  42cab7:	8b ec                	mov    ebp,esp
  42cab9:	8b 45 08             	mov    eax,DWORD PTR [ebp+0x8]
  42cabc:	8b 00                	mov    eax,DWORD PTR [eax]
  42cabe:	81 38 63 73 6d e0    	cmp    DWORD PTR [eax],0xe06d7363
  42cac4:	75 25                	jne    0x42caeb
  42cac6:	83 78 10 03          	cmp    DWORD PTR [eax+0x10],0x3
  42caca:	75 1f                	jne    0x42caeb
  42cacc:	8b 40 14             	mov    eax,DWORD PTR [eax+0x14]
  42cacf:	3d 20 05 93 19       	cmp    eax,0x19930520
  42cad4:	74 1b                	je     0x42caf1
  42cad6:	3d 21 05 93 19       	cmp    eax,0x19930521
  42cadb:	74 14                	je     0x42caf1
  42cadd:	3d 22 05 93 19       	cmp    eax,0x19930522
  42cae2:	74 0d                	je     0x42caf1
  42cae4:	3d 00 40 99 01       	cmp    eax,0x1994000
  42cae9:	74 06                	je     0x42caf1
  42caeb:	33 c0                	xor    eax,eax
  42caed:	5d                   	pop    ebp
  42caee:	c2 04 00             	ret    0x4
  42caf1:	e8 52 00 00 00       	call   0x42cb48
  42caf6:	cc                   	int3
  42caf7:	68 b6 ca 42 00       	push   0x42cab6
  42cafc:	e8 59 00 00 00       	call   0x42cb5a
  42cb01:	59                   	pop    ecx
  42cb02:	33 c0                	xor    eax,eax
  42cb04:	c3                   	ret
  42cb05:	cc                   	int3
  42cb06:	ff 25 84 00 43 00    	jmp    DWORD PTR ds:0x430084
  42cb0c:	33 c0                	xor    eax,eax
  42cb0e:	c3                   	ret
  42cb0f:	56                   	push   esi
  42cb10:	68 00 00 03 00       	push   0x30000
  42cb15:	68 00 00 01 00       	push   0x10000
  42cb1a:	33 f6                	xor    esi,esi
  42cb1c:	56                   	push   esi
  42cb1d:	e8 44 00 00 00       	call   0x42cb66
  42cb22:	83 c4 0c             	add    esp,0xc
  42cb25:	85 c0                	test   eax,eax
  42cb27:	75 02                	jne    0x42cb2b
  42cb29:	5e                   	pop    esi
  42cb2a:	c3                   	ret
  42cb2b:	56                   	push   esi
  42cb2c:	56                   	push   esi
  42cb2d:	56                   	push   esi
  42cb2e:	56                   	push   esi
  42cb2f:	56                   	push   esi
  42cb30:	e8 2b 00 00 00       	call   0x42cb60
  42cb35:	cc                   	int3
  42cb36:	ff 25 b8 00 43 00    	jmp    DWORD PTR ds:0x4300b8
  42cb3c:	ff 25 bc 00 43 00    	jmp    DWORD PTR ds:0x4300bc
  42cb42:	ff 25 c0 00 43 00    	jmp    DWORD PTR ds:0x4300c0
  42cb48:	ff 25 c4 00 43 00    	jmp    DWORD PTR ds:0x4300c4
  42cb4e:	ff 25 c8 00 43 00    	jmp    DWORD PTR ds:0x4300c8
  42cb54:	ff 25 cc 00 43 00    	jmp    DWORD PTR ds:0x4300cc
  42cb5a:	ff 25 d0 00 43 00    	jmp    DWORD PTR ds:0x4300d0
  42cb60:	ff 25 d8 00 43 00    	jmp    DWORD PTR ds:0x4300d8
  42cb66:	ff 25 dc 00 43 00    	jmp    DWORD PTR ds:0x4300dc
  42cb6c:	ff 25 10 01 43 00    	jmp    DWORD PTR ds:0x430110
  42cb72:	ff 25 00 01 43 00    	jmp    DWORD PTR ds:0x430100
  42cb78:	ff 25 04 01 43 00    	jmp    DWORD PTR ds:0x430104
  42cb7e:	ff 25 08 01 43 00    	jmp    DWORD PTR ds:0x430108
  42cb84:	ff 25 18 01 43 00    	jmp    DWORD PTR ds:0x430118
  42cb8a:	ff 25 14 01 43 00    	jmp    DWORD PTR ds:0x430114
  42cb90:	ff 25 fc 00 43 00    	jmp    DWORD PTR ds:0x4300fc
  42cb96:	ff 25 0c 01 43 00    	jmp    DWORD PTR ds:0x43010c
  42cb9c:	ff 25 20 01 43 00    	jmp    DWORD PTR ds:0x430120
  42cba2:	ff 25 24 01 43 00    	jmp    DWORD PTR ds:0x430124
  42cba8:	ff 25 2c 01 43 00    	jmp    DWORD PTR ds:0x43012c
  42cbae:	ff 25 1c 00 43 00    	jmp    DWORD PTR ds:0x43001c
  42cbb4:	e8 ed 00 00 00       	call   0x42cca6
  42cbb9:	c2 10 00             	ret    0x10
  42cbbc:	6a 00                	push   0x0
  42cbbe:	b8 f2 cd 42 00       	mov    eax,0x42cdf2
  42cbc3:	e8 8d f9 ff ff       	call   0x42c555
  42cbc8:	8b 7d 08             	mov    edi,DWORD PTR [ebp+0x8]
  42cbcb:	ff 75 0c             	push   DWORD PTR [ebp+0xc]
  42cbce:	8d 77 10             	lea    esi,[edi+0x10]
  42cbd1:	56                   	push   esi
  42cbd2:	e8 62 00 00 00       	call   0x42cc39
  42cbd7:	59                   	pop    ecx
  42cbd8:	59                   	pop    ecx
  42cbd9:	83 65 fc 00          	and    DWORD PTR [ebp-0x4],0x0
  42cbdd:	57                   	push   edi
  42cbde:	c7 07 a0 c2 43 00    	mov    DWORD PTR [edi],0x43c2a0
  42cbe4:	c7 47 04 c4 c2 43 00 	mov    DWORD PTR [edi+0x4],0x43c2c4
  42cbeb:	c7 47 08 e0 c2 43 00 	mov    DWORD PTR [edi+0x8],0x43c2e0
  42cbf2:	c7 47 0c fc c2 43 00 	mov    DWORD PTR [edi+0xc],0x43c2fc
  42cbf9:	c7 06 20 c3 43 00    	mov    DWORD PTR [esi],0x43c320
  42cbff:	c7 47 14 3c c3 43 00 	mov    DWORD PTR [edi+0x14],0x43c33c
  42cc06:	c7 47 18 60 c3 43 00 	mov    DWORD PTR [edi+0x18],0x43c360
  42cc0d:	c7 47 1c 7c c3 43 00 	mov    DWORD PTR [edi+0x1c],0x43c37c
  42cc14:	c7 47 20 94 c3 43 00 	mov    DWORD PTR [edi+0x20],0x43c394
  42cc1b:	c7 47 3c b0 c3 43 00 	mov    DWORD PTR [edi+0x3c],0x43c3b0
  42cc22:	c7 47 40 c8 c3 43 00 	mov    DWORD PTR [edi+0x40],0x43c3c8
  42cc29:	e8 08 f1 ff ff       	call   0x42bd36
  42cc2e:	89 47 04             	mov    DWORD PTR [edi+0x4],eax
  42cc31:	8b c7                	mov    eax,edi
  42cc33:	e8 09 f9 ff ff       	call   0x42c541
  42cc38:	c3                   	ret
  42cc39:	6a 00                	push   0x0
  42cc3b:	b8 18 ce 42 00       	mov    eax,0x42ce18
  42cc40:	e8 10 f9 ff ff       	call   0x42c555
  42cc45:	8b 7d 08             	mov    edi,DWORD PTR [ebp+0x8]
  42cc48:	8d 77 08             	lea    esi,[edi+0x8]
  42cc4b:	56                   	push   esi
  42cc4c:	e8 17 ee ff ff       	call   0x42ba68
  42cc51:	59                   	pop    ecx
  42cc52:	33 db                	xor    ebx,ebx
  42cc54:	57                   	push   edi
  42cc55:	8d 4f 20             	lea    ecx,[edi+0x20]
  42cc58:	c7 07 10 c2 43 00    	mov    DWORD PTR [edi],0x43c210
  42cc5e:	c7 47 04 2c c2 43 00 	mov    DWORD PTR [edi+0x4],0x43c22c
  42cc65:	c7 06 50 c2 43 00    	mov    DWORD PTR [esi],0x43c250
  42cc6b:	c7 47 0c 6c c2 43 00 	mov    DWORD PTR [edi+0xc],0x43c26c
  42cc72:	c7 47 10 84 c2 43 00 	mov    DWORD PTR [edi+0x10],0x43c284
  42cc79:	89 5f 14             	mov    DWORD PTR [edi+0x14],ebx
  42cc7c:	88 5f 18             	mov    BYTE PTR [edi+0x18],bl
  42cc7f:	89 5f 1c             	mov    DWORD PTR [edi+0x1c],ebx
  42cc82:	e8 39 6d fe ff       	call   0x4139c0
  42cc87:	8b 75 0c             	mov    esi,DWORD PTR [ebp+0xc]
  42cc8a:	89 5d fc             	mov    DWORD PTR [ebp-0x4],ebx
  42cc8d:	85 f6                	test   esi,esi
  42cc8f:	74 0d                	je     0x42cc9e
  42cc91:	56                   	push   esi
  42cc92:	e8 59 dd ff ff       	call   0x42a9f0
  42cc97:	59                   	pop    ecx
  42cc98:	89 47 1c             	mov    DWORD PTR [edi+0x1c],eax
  42cc9b:	89 77 14             	mov    DWORD PTR [edi+0x14],esi
  42cc9e:	8b c7                	mov    eax,edi
  42cca0:	e8 9c f8 ff ff       	call   0x42c541
  42cca5:	c3                   	ret
  42cca6:	6a 1c                	push   0x1c
  42cca8:	b8 68 ce 42 00       	mov    eax,0x42ce68
  42ccad:	e8 a3 f8 ff ff       	call   0x42c555
  42ccb2:	83 65 f0 00          	and    DWORD PTR [ebp-0x10],0x0
  42ccb6:	8d 45 f0             	lea    eax,[ebp-0x10]
  42ccb9:	50                   	push   eax
  42ccba:	e8 cf 00 00 00       	call   0x42cd8e
  42ccbf:	8b f0                	mov    esi,eax
  42ccc1:	6a 48                	push   0x48
  42ccc3:	89 75 e8             	mov    DWORD PTR [ebp-0x18],esi
  42ccc6:	e8 5b f0 ff ff       	call   0x42bd26
  42cccb:	89 45 e4             	mov    DWORD PTR [ebp-0x1c],eax
  42ccce:	ff 75 f0             	push   DWORD PTR [ebp-0x10]
  42ccd1:	83 65 fc 00          	and    DWORD PTR [ebp-0x4],0x0
  42ccd5:	50                   	push   eax
  42ccd6:	e8 e1 fe ff ff       	call   0x42cbbc
  42ccdb:	8b f8                	mov    edi,eax
  42ccdd:	83 c4 10             	add    esp,0x10
  42cce0:	89 7d e4             	mov    DWORD PTR [ebp-0x1c],edi
  42cce3:	89 7d e0             	mov    DWORD PTR [ebp-0x20],edi
  42cce6:	33 db                	xor    ebx,ebx
  42cce8:	c7 45 fc 03 00 00 00 	mov    DWORD PTR [ebp-0x4],0x3
  42ccef:	39 5d f0             	cmp    DWORD PTR [ebp-0x10],ebx
  42ccf2:	7e 40                	jle    0x42cd34
  42ccf4:	21 5d dc             	and    DWORD PTR [ebp-0x24],ebx
  42ccf7:	8d 47 10             	lea    eax,[edi+0x10]
  42ccfa:	8b f8                	mov    edi,eax
  42ccfc:	ff 34 9e             	push   DWORD PTR [esi+ebx*4]
  42ccff:	c6 45 fc 04          	mov    BYTE PTR [ebp-0x4],0x4
  42cd03:	6a 00                	push   0x0
  42cd05:	e8 76 f8 fe ff       	call   0x41c580
  42cd0a:	8b f0                	mov    esi,eax
  42cd0c:	89 75 ec             	mov    DWORD PTR [ebp-0x14],esi
  42cd0f:	56                   	push   esi
  42cd10:	53                   	push   ebx
  42cd11:	57                   	push   edi
  42cd12:	c6 45 fc 06          	mov    BYTE PTR [ebp-0x4],0x6
  42cd16:	e8 38 00 00 00       	call   0x42cd53
  42cd1b:	83 c4 14             	add    esp,0x14
  42cd1e:	c6 45 fc 03          	mov    BYTE PTR [ebp-0x4],0x3
  42cd22:	56                   	push   esi
  42cd23:	e8 4a fe ff ff       	call   0x42cb72
  42cd28:	8b 75 e8             	mov    esi,DWORD PTR [ebp-0x18]
  42cd2b:	43                   	inc    ebx
  42cd2c:	3b 5d f0             	cmp    ebx,DWORD PTR [ebp-0x10]
  42cd2f:	7c cb                	jl     0x42ccfc
  42cd31:	8b 7d e4             	mov    edi,DWORD PTR [ebp-0x1c]
  42cd34:	57                   	push   edi
  42cd35:	e8 c6 59 ff ff       	call   0x422700
  42cd3a:	83 4d fc ff          	or     DWORD PTR [ebp-0x4],0xffffffff
  42cd3e:	59                   	pop    ecx
  42cd3f:	8b f0                	mov    esi,eax
  42cd41:	85 ff                	test   edi,edi
  42cd43:	74 06                	je     0x42cd4b
  42cd45:	8b 0f                	mov    ecx,DWORD PTR [edi]
  42cd47:	57                   	push   edi
  42cd48:	ff 51 08             	call   DWORD PTR [ecx+0x8]
  42cd4b:	8b c6                	mov    eax,esi
  42cd4d:	e8 ef f7 ff ff       	call   0x42c541
  42cd52:	c3                   	ret
  42cd53:	55                   	push   ebp
  42cd54:	8b ec                	mov    ebp,esp
  42cd56:	56                   	push   esi
  42cd57:	57                   	push   edi
  42cd58:	8b 7d 08             	mov    edi,DWORD PTR [ebp+0x8]
  42cd5b:	8b 47 1c             	mov    eax,DWORD PTR [edi+0x1c]
  42cd5e:	85 c0                	test   eax,eax
  42cd60:	74 21                	je     0x42cd83
  42cd62:	8b 75 0c             	mov    esi,DWORD PTR [ebp+0xc]
  42cd65:	3b 77 14             	cmp    esi,DWORD PTR [edi+0x14]
  42cd68:	73 1e                	jae    0x42cd88
  42cd6a:	ff 75 10             	push   DWORD PTR [ebp+0x10]
  42cd6d:	c1 e6 02             	shl    esi,0x2
  42cd70:	03 c6                	add    eax,esi
  42cd72:	50                   	push   eax
  42cd73:	e8 08 5a fe ff       	call   0x412780
  42cd78:	8b 47 1c             	mov    eax,DWORD PTR [edi+0x1c]
  42cd7b:	59                   	pop    ecx
  42cd7c:	59                   	pop    ecx
  42cd7d:	5f                   	pop    edi
  42cd7e:	03 c6                	add    eax,esi
  42cd80:	5e                   	pop    esi
  42cd81:	5d                   	pop    ebp
  42cd82:	c3                   	ret
  42cd83:	e8 80 ef ff ff       	call   0x42bd08
  42cd88:	e8 75 ef ff ff       	call   0x42bd02
  42cd8d:	cc                   	int3
  42cd8e:	ff 25 f8 01 43 00    	jmp    DWORD PTR ds:0x4301f8
  42cd94:	ff 25 e0 00 43 00    	jmp    DWORD PTR ds:0x4300e0
  42cd9a:	ff 35 a0 fc 43 00    	push   DWORD PTR ds:0x43fca0
  42cda0:	e8 29 00 00 00       	call   0x42cdce
  42cda5:	33 c9                	xor    ecx,ecx
  42cda7:	84 c0                	test   al,al
  42cda9:	0f 94 c1             	sete   cl
  42cdac:	8b c1                	mov    eax,ecx
  42cdae:	c3                   	ret
  42cdaf:	55                   	push   ebp
  42cdb0:	8b ec                	mov    ebp,esp
  42cdb2:	ff 75 0c             	push   DWORD PTR [ebp+0xc]
  42cdb5:	ff 75 08             	push   DWORD PTR [ebp+0x8]
  42cdb8:	ff 35 a0 fc 43 00    	push   DWORD PTR ds:0x43fca0
  42cdbe:	e8 05 00 00 00       	call   0x42cdc8
  42cdc3:	5d                   	pop    ebp
  42cdc4:	c2 08 00             	ret    0x8
  42cdc7:	cc                   	int3
  42cdc8:	ff 25 00 02 43 00    	jmp    DWORD PTR ds:0x430200
  42cdce:	ff 25 04 02 43 00    	jmp    DWORD PTR ds:0x430204
  42cdd4:	ff 25 d4 00 43 00    	jmp    DWORD PTR ds:0x4300d4
  42cdda:	cc                   	int3
  42cddb:	cc                   	int3
  42cddc:	cc                   	int3
  42cddd:	cc                   	int3
  42cdde:	cc                   	int3
  42cddf:	cc                   	int3
  42cde0:	8b 4d 08             	mov    ecx,DWORD PTR [ebp+0x8]
  42cde3:	83 c1 14             	add    ecx,0x14
  42cde6:	8b 45 08             	mov    eax,DWORD PTR [ebp+0x8]
  42cde9:	8b 40 14             	mov    eax,DWORD PTR [eax+0x14]
  42cdec:	51                   	push   ecx
  42cded:	ff 50 1c             	call   DWORD PTR [eax+0x1c]

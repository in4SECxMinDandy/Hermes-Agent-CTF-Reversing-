
workspace/appx/MetroApp.exe:     file format pei-i386


Disassembly of section .text:

004144a0 <.text+0x134a0>:
  4144a0:	e5 5d                	in     eax,0x5d
  4144a2:	c3                   	ret
  4144a3:	cc                   	int3
  4144a4:	cc                   	int3
  4144a5:	cc                   	int3
  4144a6:	cc                   	int3
  4144a7:	cc                   	int3
  4144a8:	cc                   	int3
  4144a9:	cc                   	int3
  4144aa:	cc                   	int3
  4144ab:	cc                   	int3
  4144ac:	cc                   	int3
  4144ad:	cc                   	int3
  4144ae:	cc                   	int3
  4144af:	cc                   	int3
  4144b0:	55                   	push   ebp
  4144b1:	8b ec                	mov    ebp,esp
  4144b3:	6a ff                	push   0xffffffff
  4144b5:	68 11 cf 42 00       	push   0x42cf11
  4144ba:	64 a1 00 00 00 00    	mov    eax,fs:0x0
  4144c0:	50                   	push   eax
  4144c1:	83 ec 20             	sub    esp,0x20
  4144c4:	a1 f4 c1 43 00       	mov    eax,ds:0x43c1f4
  4144c9:	33 c5                	xor    eax,ebp
  4144cb:	89 45 f0             	mov    DWORD PTR [ebp-0x10],eax
  4144ce:	56                   	push   esi
  4144cf:	57                   	push   edi
  4144d0:	50                   	push   eax
  4144d1:	8d 45 f4             	lea    eax,[ebp-0xc]
  4144d4:	64 a3 00 00 00 00    	mov    fs:0x0,eax
  4144da:	8b f2                	mov    esi,edx
  4144dc:	8b 7d 08             	mov    edi,DWORD PTR [ebp+0x8]
  4144df:	c7 45 e0 77 17 16 2d 	mov    DWORD PTR [ebp-0x20],0x2d161777
  4144e6:	c7 45 e4 6f a6 a5 4e 	mov    DWORD PTR [ebp-0x1c],0x4ea5a66f
  4144ed:	c7 45 e8 bb 87 79 3f 	mov    DWORD PTR [ebp-0x18],0x3f7987bb
  4144f4:	c7 45 ec fa 49 41 f2 	mov    DWORD PTR [ebp-0x14],0xf24149fa
  4144fb:	c7 45 dc 00 00 00 00 	mov    DWORD PTR [ebp-0x24],0x0
  414502:	8d 45 dc             	lea    eax,[ebp-0x24]
  414505:	50                   	push   eax
  414506:	8d 45 e0             	lea    eax,[ebp-0x20]
  414509:	50                   	push   eax
  41450a:	68 68 09 43 00       	push   0x430968
  41450f:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [ebp-0x4],0x0
  414516:	e8 11 78 01 00       	call   0x42bd2c
  41451b:	85 c0                	test   eax,eax
  41451d:	79 06                	jns    0x414525
  41451f:	50                   	push   eax
  414520:	e8 bb f3 ff ff       	call   0x4138e0
  414525:	57                   	push   edi
  414526:	56                   	push   esi
  414527:	ff 75 dc             	push   DWORD PTR [ebp-0x24]
  41452a:	e8 e1 00 00 00       	call   0x414610
  41452f:	83 c4 0c             	add    esp,0xc
  414532:	8b f0                	mov    esi,eax
  414534:	c7 45 fc ff ff ff ff 	mov    DWORD PTR [ebp-0x4],0xffffffff
  41453b:	8b 55 dc             	mov    edx,DWORD PTR [ebp-0x24]
  41453e:	85 d2                	test   edx,edx
  414540:	74 06                	je     0x414548
  414542:	8b 0a                	mov    ecx,DWORD PTR [edx]
  414544:	52                   	push   edx
  414545:	ff 51 08             	call   DWORD PTR [ecx+0x8]
  414548:	8b c6                	mov    eax,esi
  41454a:	8b 4d f4             	mov    ecx,DWORD PTR [ebp-0xc]
  41454d:	64 89 0d 00 00 00 00 	mov    DWORD PTR fs:0x0,ecx
  414554:	59                   	pop    ecx
  414555:	5f                   	pop    edi
  414556:	5e                   	pop    esi
  414557:	8b 4d f0             	mov    ecx,DWORD PTR [ebp-0x10]
  41455a:	33 cd                	xor    ecx,ebp
  41455c:	e8 2c 78 01 00       	call   0x42bd8d
  414561:	8b e5                	mov    esp,ebp
  414563:	5d                   	pop    ebp
  414564:	c3                   	ret
  414565:	cc                   	int3
  414566:	cc                   	int3
  414567:	cc                   	int3
  414568:	cc                   	int3
  414569:	cc                   	int3
  41456a:	cc                   	int3
  41456b:	cc                   	int3
  41456c:	cc                   	int3
  41456d:	cc                   	int3
  41456e:	cc                   	int3
  41456f:	cc                   	int3
  414570:	55                   	push   ebp
  414571:	8b ec                	mov    ebp,esp
  414573:	6a ff                	push   0xffffffff
  414575:	68 db ed 42 00       	push   0x42eddb
  41457a:	64 a1 00 00 00 00    	mov    eax,fs:0x0
  414580:	50                   	push   eax
  414581:	83 ec 08             	sub    esp,0x8
  414584:	a1 f4 c1 43 00       	mov    eax,ds:0x43c1f4
  414589:	33 c5                	xor    eax,ebp
  41458b:	89 45 f0             	mov    DWORD PTR [ebp-0x10],eax
  41458e:	56                   	push   esi
  41458f:	50                   	push   eax
  414590:	8d 45 f4             	lea    eax,[ebp-0xc]
  414593:	64 a3 00 00 00 00    	mov    fs:0x0,eax
  414599:	8b 55 08             	mov    edx,DWORD PTR [ebp+0x8]
  41459c:	8b 4d 0c             	mov    ecx,DWORD PTR [ebp+0xc]
  41459f:	c7 45 ec 00 00 00 00 	mov    DWORD PTR [ebp-0x14],0x0
  4145a6:	8d 75 ec             	lea    esi,[ebp-0x14]
  4145a9:	56                   	push   esi
  4145aa:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [ebp-0x4],0x0
  4145b1:	8b 02                	mov    eax,DWORD PTR [edx]
  4145b3:	51                   	push   ecx
  4145b4:	52                   	push   edx
  4145b5:	ff 50 18             	call   DWORD PTR [eax+0x18]
  4145b8:	85 c0                	test   eax,eax
  4145ba:	79 06                	jns    0x4145c2
  4145bc:	50                   	push   eax
  4145bd:	e8 1e f3 ff ff       	call   0x4138e0
  4145c2:	8b 55 ec             	mov    edx,DWORD PTR [ebp-0x14]
  4145c5:	8b f2                	mov    esi,edx
  4145c7:	85 d2                	test   edx,edx
  4145c9:	74 09                	je     0x4145d4
  4145cb:	8b 02                	mov    eax,DWORD PTR [edx]
  4145cd:	52                   	push   edx
  4145ce:	ff 50 04             	call   DWORD PTR [eax+0x4]
  4145d1:	8b 55 ec             	mov    edx,DWORD PTR [ebp-0x14]
  4145d4:	c7 45 fc ff ff ff ff 	mov    DWORD PTR [ebp-0x4],0xffffffff
  4145db:	85 d2                	test   edx,edx
  4145dd:	74 06                	je     0x4145e5
  4145df:	8b 0a                	mov    ecx,DWORD PTR [edx]
  4145e1:	52                   	push   edx
  4145e2:	ff 51 08             	call   DWORD PTR [ecx+0x8]
  4145e5:	8b c6                	mov    eax,esi
  4145e7:	8b 4d f4             	mov    ecx,DWORD PTR [ebp-0xc]
  4145ea:	64 89 0d 00 00 00 00 	mov    DWORD PTR fs:0x0,ecx
  4145f1:	59                   	pop    ecx
  4145f2:	5e                   	pop    esi
  4145f3:	8b 4d f0             	mov    ecx,DWORD PTR [ebp-0x10]
  4145f6:	33 cd                	xor    ecx,ebp
  4145f8:	e8 90 77 01 00       	call   0x42bd8d
  4145fd:	8b e5                	mov    esp,ebp
  4145ff:	5d                   	pop    ebp
  414600:	c3                   	ret
  414601:	cc                   	int3
  414602:	cc                   	int3
  414603:	cc                   	int3
  414604:	cc                   	int3
  414605:	cc                   	int3
  414606:	cc                   	int3
  414607:	cc                   	int3
  414608:	cc                   	int3
  414609:	cc                   	int3
  41460a:	cc                   	int3
  41460b:	cc                   	int3
  41460c:	cc                   	int3
  41460d:	cc                   	int3
  41460e:	cc                   	int3
  41460f:	cc                   	int3
  414610:	55                   	push   ebp
  414611:	8b ec                	mov    ebp,esp
  414613:	6a ff                	push   0xffffffff
  414615:	68 1b d9 42 00       	push   0x42d91b
  41461a:	64 a1 00 00 00 00    	mov    eax,fs:0x0
  414620:	50                   	push   eax
  414621:	83 ec 08             	sub    esp,0x8
  414624:	a1 f4 c1 43 00       	mov    eax,ds:0x43c1f4
  414629:	33 c5                	xor    eax,ebp
  41462b:	89 45 f0             	mov    DWORD PTR [ebp-0x10],eax
  41462e:	56                   	push   esi
  41462f:	57                   	push   edi
  414630:	50                   	push   eax
  414631:	8d 45 f4             	lea    eax,[ebp-0xc]
  414634:	64 a3 00 00 00 00    	mov    fs:0x0,eax
  41463a:	8b 75 08             	mov    esi,DWORD PTR [ebp+0x8]
  41463d:	8b 55 0c             	mov    edx,DWORD PTR [ebp+0xc]
  414640:	8b 4d 10             	mov    ecx,DWORD PTR [ebp+0x10]
  414643:	c7 45 ec 00 00 00 00 	mov    DWORD PTR [ebp-0x14],0x0
  41464a:	8d 7d ec             	lea    edi,[ebp-0x14]
  41464d:	57                   	push   edi
  41464e:	51                   	push   ecx
  41464f:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [ebp-0x4],0x0
  414656:	8b 06                	mov    eax,DWORD PTR [esi]
  414658:	52                   	push   edx
  414659:	56                   	push   esi
  41465a:	ff 50 1c             	call   DWORD PTR [eax+0x1c]
  41465d:	85 c0                	test   eax,eax
  41465f:	79 06                	jns    0x414667
  414661:	50                   	push   eax
  414662:	e8 79 f2 ff ff       	call   0x4138e0
  414667:	8b 55 ec             	mov    edx,DWORD PTR [ebp-0x14]
  41466a:	8b f2                	mov    esi,edx
  41466c:	85 d2                	test   edx,edx
  41466e:	74 09                	je     0x414679
  414670:	8b 02                	mov    eax,DWORD PTR [edx]
  414672:	52                   	push   edx
  414673:	ff 50 04             	call   DWORD PTR [eax+0x4]
  414676:	8b 55 ec             	mov    edx,DWORD PTR [ebp-0x14]
  414679:	c7 45 fc ff ff ff ff 	mov    DWORD PTR [ebp-0x4],0xffffffff
  414680:	85 d2                	test   edx,edx
  414682:	74 06                	je     0x41468a
  414684:	8b 0a                	mov    ecx,DWORD PTR [edx]
  414686:	52                   	push   edx
  414687:	ff 51 08             	call   DWORD PTR [ecx+0x8]
  41468a:	8b c6                	mov    eax,esi
  41468c:	8b 4d f4             	mov    ecx,DWORD PTR [ebp-0xc]
  41468f:	64 89 0d 00 00 00 00 	mov    DWORD PTR fs:0x0,ecx
  414696:	59                   	pop    ecx
  414697:	5f                   	pop    edi
  414698:	5e                   	pop    esi
  414699:	8b 4d f0             	mov    ecx,DWORD PTR [ebp-0x10]
  41469c:	33 cd                	xor    ecx,ebp
  41469e:	e8 ea 76 01 00       	call   0x42bd8d
  4146a3:	8b e5                	mov    esp,ebp
  4146a5:	5d                   	pop    ebp
  4146a6:	c3                   	ret
  4146a7:	81 6c 24 04 c8 00 00 	sub    DWORD PTR [esp+0x4],0xc8
  4146ae:	00 
  4146af:	e9 4c d7 fe ff       	jmp    0x401e00
  4146b4:	81 6c 24 04 a8 00 00 	sub    DWORD PTR [esp+0x4],0xa8
  4146bb:	00 
  4146bc:	e9 cf 6f ff ff       	jmp    0x40b690
  4146c1:	83 6c 24 04 0c       	sub    DWORD PTR [esp+0x4],0xc
  4146c6:	e9 05 5e ff ff       	jmp    0x40a4d0
  4146cb:	83 6c 24 04 14       	sub    DWORD PTR [esp+0x4],0x14
  4146d0:	e9 3b 23 ff ff       	jmp    0x406a10
  4146d5:	83 6c 24 04 14       	sub    DWORD PTR [esp+0x4],0x14
  4146da:	e9 e1 18 ff ff       	jmp    0x405fc0
  4146df:	83                   	.byte 0x83

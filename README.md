# optgrouper
## optgrouper_spring8.py
* SPring-8のcryoARMで撮影した画像をcryoSPARCで処理したときに、ファイル名中のタイムスタンプを使ってexposure groupを細かく分割する処理を行います。
* 既に存在するexposure groupがさらに分割されるだけです。混ざったりはしません。

### Usage
* cryoSPARCのpython環境を利用するので、cryosparc_workerディレクトリのパスを確認してください。
* Worker bin pathから bin/cryosparcw を除いたものがcryosparc_workerディレクトリです。

![image](https://user-images.githubusercontent.com/49423083/223711276-d1fe3b58-a215-4a5d-b36c-66168e50b1ff.png)


```
PYTHONPATH=<cryosparc_worker directory path> <cryosparc_worker directory path>/deps/anaconda/envs/cryosparc_worker_env/bin/python <optgrouper directory path>/optgrouper_spring8.py --help
```

### Example
```
> PYTHONPATH=/amorphous/cryosparcuser/cryosparc/cryosparc_worker /amorphous/cryosparcuser/cryosparc/cryosparc_worker/deps/anaconda/envs/cryosparc_worker_env/bin/python ../optgrouper/optgrouper_spring8.py --infile-cs ./J119_007_particles.cs --infile-passthrough ./J119_passthrough_particles.cs --outfile hoge.cs --grouping-times 2022-10-23_03_54_36 2022-10-23_12_00_00 --grouping-hours 3 --min-ptcls-per-group 200
##### Command #####
        ../optgrouper/optgrouper_spring8.py --infile-cs ./J119_007_particles.cs --infile-passthrough ./J119_passthrough_particles.cs --outfile hoge.cs --grouping-times 2022-10-23_03_54_36 2022-10-23_12_00_00 --grouping-hours 3 --min-ptcls-per-group 200
##### Input parameters #####
        infile_cs : ./J119_007_particles.cs
        infile_passthrough : ./J119_passthrough_particles.cs
        outfile : hoge.cs
        grouping_times : ['2022-10-23_03_54_36', '2022-10-23_12_00_00']
        grouping_hours : 3.0
        min_ptcls_per_group : 200
        overwrite : False
        verbose : False

Grouping by grouping_timestamps...
Grouping by grouping_hours...


Exposure groups were re-grouped from 50 groups to 458 groups.

Exposure group 0 (#ptcls=4461) was divided into 10 groups: [0 1 2 3 4 5 6 7 8 9] (#ptcls=[201 733 530 744 499 475 320 364 320 275])
Exposure group 1 (#ptcls=4090) was divided into 10 groups: [10 11 12 13 14 15 16 17 18 19] (#ptcls=[201 690 510 725 462 410 337 278 228 249])
Exposure group 2 (#ptcls=4611) was divided into 11 groups: [20 21 22 23 24 25 26 27 28 29 30] (#ptcls=[201 770 660 645 206 444 313 229 433 374 336])
Exposure group 3 (#ptcls=3031) was divided into 9 groups: [31 32 33 34 35 36 37 38 39] (#ptcls=[201 618 240 374 512 380 218 212 276])
Exposure group 4 (#ptcls=4679) was divided into 11 groups: [40 41 42 43 44 45 46 47 48 49 50] (#ptcls=[201 743 656 607 243 493 376 240 413 396 311])
Exposure group 5 (#ptcls=3209) was divided into 9 groups: [51 52 53 54 55 56 57 58 59] (#ptcls=[201 613 364 502 498 337 210 201 283])
Exposure group 6 (#ptcls=3321) was divided into 8 groups: [60 61 62 63 64 65 66 67] (#ptcls=[201 568 337 558 515 514 219 409])
Exposure group 7 (#ptcls=4532) was divided into 10 groups: [68 69 70 71 72 73 74 75 76 77] (#ptcls=[201 721 538 763 518 376 336 362 384 333])
Exposure group 8 (#ptcls=4339) was divided into 10 groups: [78 79 80 81 82 83 84 85 86 87] (#ptcls=[201 540 524 894 448 314 303 413 369 333])
Exposure group 9 (#ptcls=4348) was divided into 10 groups: [88 89 90 91 92 93 94 95 96 97] (#ptcls=[201 628 546 803 461 371 297 376 352 313])
Exposure group 10 (#ptcls=4524) was divided into 10 groups: [ 98  99 100 101 102 103 104 105 106 107] (#ptcls=[201 623 592 882 443 382 366 402 352 281])
Exposure group 11 (#ptcls=4587) was divided into 10 groups: [108 109 110 111 112 113 114 115 116 117] (#ptcls=[201 679 622 840 523 422 349 428 285 238])
Exposure group 12 (#ptcls=4338) was divided into 10 groups: [118 119 120 121 122 123 124 125 126 127] (#ptcls=[201 829 508 595 450 434 295 402 365 259])
Exposure group 13 (#ptcls=4232) was divided into 9 groups: [128 129 130 131 132 133 134 135 136] (#ptcls=[201 781 557 714 493 454 369 257 406])
Exposure group 14 (#ptcls=4163) was divided into 9 groups: [137 138 139 140 141 142 143 144 145] (#ptcls=[201 772 616 764 375 517 363 306 249])
Exposure group 15 (#ptcls=3148) was divided into 9 groups: [146 147 148 149 150 151 152 153 154] (#ptcls=[201 516 365 393 500 442 293 219 219])
Exposure group 16 (#ptcls=2677) was divided into 8 groups: [155 156 157 158 159 160 161 162] (#ptcls=[201 438 381 635 224 241 283 274])
Exposure group 17 (#ptcls=3271) was divided into 10 groups: [163 164 165 166 167 168 169 170 171 172] (#ptcls=[201 625 463 463 223 302 280 274 232 208])
Exposure group 18 (#ptcls=2277) was divided into 6 groups: [173 174 175 176 177 178] (#ptcls=[201 515 342 465 405 349])
Exposure group 19 (#ptcls=3623) was divided into 10 groups: [179 180 181 182 183 184 185 186 187 188] (#ptcls=[201 670 551 455 236 373 373 310 240 214])
Exposure group 20 (#ptcls=3797) was divided into 10 groups: [189 190 191 192 193 194 195 196 197 198] (#ptcls=[201 747 458 476 233 424 400 318 325 215])
Exposure group 21 (#ptcls=2388) was divided into 7 groups: [199 200 201 202 203 204 205] (#ptcls=[201 470 201 300 523 370 323])
Exposure group 22 (#ptcls=3841) was divided into 10 groups: [206 207 208 209 210 211 212 213 214 215] (#ptcls=[201 768 457 435 247 407 471 348 294 213])
Exposure group 23 (#ptcls=4560) was divided into 11 groups: [216 217 218 219 220 221 222 223 224 225 226] (#ptcls=[201 848 535 551 256 609 353 256 342 364 245])
Exposure group 24 (#ptcls=3802) was divided into 10 groups: [227 228 229 230 231 232 233 234 235 236] (#ptcls=[201 622 338 707 572 309 220 296 290 247])
Exposure group 25 (#ptcls=4457) was divided into 10 groups: [237 238 239 240 241 242 243 244 245 246] (#ptcls=[201 625 485 884 612 357 301 326 341 325])
Exposure group 26 (#ptcls=4187) was divided into 10 groups: [247 248 249 250 251 252 253 254 255 256] (#ptcls=[201 570 548 804 431 262 264 371 409 327])
Exposure group 27 (#ptcls=2908) was divided into 9 groups: [257 258 259 260 261 262 263 264 265] (#ptcls=[201 300 481 622 300 282 236 275 211])
Exposure group 28 (#ptcls=3256) was divided into 9 groups: [266 267 268 269 270 271 272 273 274] (#ptcls=[201 368 483 586 335 380 328 335 240])
Exposure group 29 (#ptcls=3484) was divided into 9 groups: [275 276 277 278 279 280 281 282 283] (#ptcls=[201 416 507 600 349 488 335 327 261])
Exposure group 30 (#ptcls=3782) was divided into 10 groups: [284 285 286 287 288 289 290 291 292 293] (#ptcls=[201 476 534 687 390 313 255 380 303 243])
Exposure group 31 (#ptcls=3796) was divided into 10 groups: [294 295 296 297 298 299 300 301 302 303] (#ptcls=[201 463 499 712 410 357 276 339 282 257])
Exposure group 32 (#ptcls=4778) was divided into 10 groups: [304 305 306 307 308 309 310 311 312 313] (#ptcls=[201 754 506 655 599 470 349 442 436 366])
Exposure group 33 (#ptcls=4584) was divided into 10 groups: [314 315 316 317 318 319 320 321 322 323] (#ptcls=[201 777 544 550 555 490 288 422 417 340])
Exposure group 34 (#ptcls=4799) was divided into 11 groups: [324 325 326 327 328 329 330 331 332 333 334] (#ptcls=[201 784 667 617 298 541 385 259 355 401 291])
Exposure group 35 (#ptcls=4559) was divided into 11 groups: [335 336 337 338 339 340 341 342 343 344 345] (#ptcls=[201 631 596 561 206 674 446 342 302 339 261])
Exposure group 36 (#ptcls=3499) was divided into 10 groups: [346 347 348 349 350 351 352 353 354 355] (#ptcls=[201 446 352 341 651 591 237 221 220 239])
Exposure group 37 (#ptcls=3576) was divided into 10 groups: [356 357 358 359 360 361 362 363 364 365] (#ptcls=[201 538 350 337 518 642 226 319 201 244])
Exposure group 38 (#ptcls=3779) was divided into 10 groups: [366 367 368 369 370 371 372 373 374 375] (#ptcls=[201 550 394 330 553 670 203 427 232 219])
Exposure group 39 (#ptcls=2158) was divided into 6 groups: [376 377 378 379 380 381] (#ptcls=[201 429 382 470 374 302])
Exposure group 40 (#ptcls=3564) was divided into 9 groups: [382 383 384 385 386 387 388 389 390] (#ptcls=[201 483 318 510 727 506 209 209 401])
Exposure group 41 (#ptcls=4137) was divided into 9 groups: [391 392 393 394 395 396 397 398 399] (#ptcls=[201 635 585 632 609 411 289 291 484])
Exposure group 42 (#ptcls=3731) was divided into 8 groups: [400 401 402 403 404 405 406 407] (#ptcls=[201 655 396 460 721 691 201 406])
Exposure group 43 (#ptcls=2589) was divided into 8 groups: [408 409 410 411 412 413 414 415] (#ptcls=[201 448 223 267 465 565 201 219])
Exposure group 44 (#ptcls=2666) was divided into 7 groups: [416 417 418 419 420 421 422] (#ptcls=[201 444 439 547 631 201 203])
Exposure group 45 (#ptcls=2503) was divided into 6 groups: [423 424 425 426 427 428] (#ptcls=[201 437 405 442 658 360])
Exposure group 46 (#ptcls=2643) was divided into 7 groups: [429 430 431 432 433 434 435] (#ptcls=[201 358 394 573 691 201 225])
Exposure group 47 (#ptcls=2729) was divided into 7 groups: [436 437 438 439 440 441 442] (#ptcls=[201 392 319 496 750 271 300])
Exposure group 48 (#ptcls=2777) was divided into 8 groups: [443 444 445 446 447 448 449 450] (#ptcls=[201 547 201 458 535 359 201 275])
Exposure group 49 (#ptcls=2228) was divided into 7 groups: [451 452 453 454 455 456 457] (#ptcls=[201 446 354 421 321 208 277])

New dataset file was saved as hoge.cs

A csv file for checking the groups assignments was saved as hoge.csv

Histgram plot of the number of particles per group was saved as hoge.png
```

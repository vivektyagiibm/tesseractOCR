# tesseractOCR
Tesseract based OCR

An Overview of Tesseract LSTM OCR System
Vivek Tyagi 


Introduction: In this short report, we provide a brief overview of the different components in the Tesseract OCR system. We note that Tesseract is a long running open score project (over 30 years now) with several legacy techniques developed in its processing pipeline. As the author's primary research background is in Speech recognition and Text/NLP deep learning, a  comprehensive explanation of these OCR components will be outside the scope of this brief report. However we will present the deep learning components especially the convolution feature extraction layer and the LSTM character recognition layer that provides the recognized lines.  


OCR of receipts is a particularly challenging problem due to geometrical distortions and variable fonts and crumpling of the paper receipt. We now describe these components. 

Text Line Normalization: This step is accomplished by use of a dictionary composed of connected component shapes. This dictionary is precomputed based on a large sample of text lines. 

LSTM OCR: The Text line images and the corresponding ground-truth text are inputted to the LSTM network which can be bidirectional and can have multiple (1-5) hidden layers and the output layer which has a softmax layer with ‘K’ output nodes where ‘K’ is size of the letters that we will recognize. For example, for English it will be typically 80-90 characters consisting  of all lower and upper case letter, digits, blank space, and 5-8 special character such as $,+,* etc. {A-Za-z0-9*+$}   

In the training phase we input the  text line images and the corresponding ground-truth text. LSTM training progresses by outputting the posterior probability for all the “K” characters for each input time-step (typically a small region of text-line image which has been fine tuned in the Text Line Normalization step). We then use the Connectionist Temporal Classification (CTC) loss developed by Alex Graves to map the variable size input sequence (text line image) to variable size output characters. In computing CTC loss we allow all possible sequences which maps the input to the output character sequence. For example certain time steps may output multiple blank spaces and/or multiple repetition of a character and these will be merged in the CTC loss computation to map them to the provided ground-truth text. The details of the CTC loss can be found in the Alex Graves paper[1]. It is worth noting that CTC loss development [1] by Alex Graves has been a revolutionary invention and it is used in multiple variable input sequence to variable output sequence learning problems such as Speech Recognition, Neural Machine  Translation, OCR and Handwriting recognition[1,3,4]. CTC loss is also a special case of the forward backward algorithm used in the Expectation-Maximization (EM) algorithm to estimate parameters of a generative model such as Hidden markov Models and Gaussian mixture Models [2]. 

Inference: Once the LSTM OCR model has been trained, it can be used for performing OCR on a test image. Basically, the test image lines are inputted to the trained LSTM OCR model and the output character ‘j’ that has the highest probability at the output softmax layer is retained as the recognized character at this time step and the decoding proceeds to the next time step. This is called greedy decoding. We can further improve the results by performing a beam search of the output character sequence and also combining it with the words language model which further the recognition accuracy. However, it is worth noting that LSTM implicitly learns a language model (LM) too during training and hence its performance even without an explicit LM is very good. 

  
The recognition accuracy is measured in terms of Character Error rate (CER) which in trun is computed by the edit distance between the recognized character sequence and the ground-truth text character sequence. 



OCR Code


In the provided OCR code we have used Tesseract’s open source LSTM pre-trained English language model to perform OCR on the 200 receipts in our dataset. 


A visual check of the receipts showed the receipt layout varies a lot and the language and currency also varies a lot. Some receipts also had sever geometrical distortions which leads to very poor OCR for those images. 

Based on these constraints we developed the following hand-engineered rules to extract the “Restaurant Name” and the “ Total Amount” in the receipt. 

Generally the restaurant name is the first text line in a receipt. However due to the geometrical distortions and orientation variation, Tesseract OCR recognizes certain text boxes with 1-2 characters or even just black characters in the first few lines of the recognized OCR lines. Therefore, we mark the first line which has more than MIN_LENGTH_NAME alphanumeric characters as the “ Restaurant Name”. In the code we have used MIN_LENGTH_NAME=5. This serves as a good threshold as it ignores the initial OCR lines which may have just 1-2 spurious characters and/or just blank spaces in it due to the geometrical distortions and variable orientation. If the “Restaurant Name” line using the above rule is not successfully detected, we output a special token “UNK” i.e UNKNOWN as the restaurant name. 
For the total amount, we search for a OCR line that has substring “total” or ‘otal’ in it but does not have ‘subtotal’ as we want to detect the total amount and not subtotal amount. We use both the substring ‘total’ and ‘otal‘ as a match as sometimes the first character is missing in the OCR output. One we have detected such a line, we extract its last word as the total amount. This is extracted as a string due to the possible presence of the currency character as well as some 1-2 minor alphabet/special character errors. 
If the “Total amount” line using the above rule is not successfully detected, we output a special token “UNK” i.e UNKNOWN as the total amount. 
  
In these OCR experiments we can use Character error rate (CER) as the metric to estimate the OCR accuracy for both the restaurant name as well as the total amount. I couldn;t compute these CER metrics as I didn’t have the ground truth in a file and due to my current work load, I was not able to myself hand-transcribe the ground truth of these 200 receipts. However a quick manual check reveals that ~75-80% receipts were recogn zied with a valid “Restaurant name” and the “total amount”. The output from our code is provided below. 


References
[1] Graves, Alex. "Connectionist temporal classification." Supervised Sequence Labelling with Recurrent Neural Networks. Springer, Berlin, Heidelberg, 2012. 61-93.
[2] Dempster, A.P., Laird, N.M. and Rubin, D.B., 1977. Maximum likelihood from incomplete data via the EM algorithm. Journal of the Royal Statistical Society: Series B (Methodological), 39(1), pp.1-22.
[3]Sak, H., Senior, A., Rao, K., Irsoy, O., Graves, A., Beaufays, F. and Schalkwyk, J., 2015, April. Learning acoustic frame labeling for speech recognition with recurrent neural networks. In 2015 IEEE international conference on acoustics, speech and signal processing (ICASSP) (pp. 4280-4284). IEEE.
[4]Liwicki, M., Graves, A., Fernàndez, S., Bunke, H. and Schmidhuber, J., 2007. A novel approach to on-line handwriting recognition based on bidirectional long short-term memory networks. In Proceedings of the 9th International Conference on Document Analysis and Recognition, ICDAR 2007.


vtyagi@Viveks-MacBook-Pro OCR % python3 runOCR2.py


dataset/1000-receipt.jpg
Number of lines:31
Restaurant Name: GAEEN FIELD
Total: 6.5
dataset/1001-receipt.jpg
Number of lines:2
Restaurant Name: UNK
Total: UNK
dataset/1002-receipt.jpg
Number of lines:33
Restaurant Name: o Crsh Fz
Total: 78
dataset/1003-receipt.jpg
Number of lines:2
Restaurant Name: UNK
Total: UNK
dataset/1004-receipt.jpg
Number of lines:26
Restaurant Name: SOLDEN BowL TERI
Total: O3
dataset/1005-receipt.jpg
Number of lines:24
Restaurant Name: Rye 10yr (2 620.00) 40,00
Total: Total
dataset/1006-receipt.jpg
Number of lines:19
Restaurant Name: Senmont oy
Total: UNK
dataset/1007-receipt.jpg
Number of lines:30
Restaurant Name: Katana Sushi
Total: $143.71
dataset/1008-receipt.jpg
Number of lines:27
Restaurant Name: Dona Mercedes Restaurant
Total: $24.47
dataset/1009-receipt.jpg
Number of lines:34
Restaurant Name: Ayl Past
Total: Total
dataset/1010-receipt.jpg
Number of lines:57
Restaurant Name: Friendly Red' s
Total: Total
dataset/1011-receipt.jpg
Number of lines:29
Restaurant Name: Pulled Pork Sand $8.50
Total: $64.43
dataset/1012-receipt.jpg
Number of lines:35
Restaurant Name: HP Pho Ga
Total: «268
dataset/1013-receipt.jpg
Number of lines:22
Restaurant Name: ALBETOS
Total: TOTAL
dataset/1014-receipt.jpg
Number of lines:20
Restaurant Name: § ?‘Iﬂfl war Blvd
Total: UNK
dataset/1015-receipt.jpg
Number of lines:62
Restaurant Name: 7285 Roswell
Total: Total
dataset/1016-receipt.jpg
Number of lines:31
Restaurant Name: Chef Wang
Total: $35.52
dataset/1017-receipt.jpg
Number of lines:24
Restaurant Name: 4327 N. Expressway 77/83
Total: Total
dataset/1018-receipt.jpg
Number of lines:32
Restaurant Name: o 12:49 PM
Total: UNK
dataset/1019-receipt.jpg
Number of lines:35
Restaurant Name: o Pieri 4 Tavem
Total: UNK
dataset/1020-receipt.jpg
Number of lines:77
Restaurant Name: Deocan Spice
Total: TOTAL:
dataset/1021-receipt.jpg
Number of lines:26
Restaurant Name: HAWWI ETHIOPIAN RESTAU
Total: UNK
dataset/1022-receipt.jpg
Number of lines:7
Restaurant Name: Sl B\ um
Total: UNK
dataset/1023-receipt.jpg
Number of lines:41
Restaurant Name: Thai Gusto Restaurant
Total: Total
dataset/1024-receipt.jpg
Number of lines:26
Restaurant Name: New Asia Bufrfet
Total: 33.92


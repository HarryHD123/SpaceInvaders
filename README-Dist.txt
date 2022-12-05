To distribute, run the .spec file.

MyGame.spec gives only the game - Highscores do not work and before dist change the setting HS_on to 
					    false when importing the highscore files lines 73 and 74

MyGame_withHighScores.spec 	  - Highscores do work, before dist change the setting HS_on to 
					    true when importing the highscore files lines 73 and 74.
					    Once dist folder is built, copy in the HighScores folder.
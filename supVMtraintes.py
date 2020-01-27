'''
  saved_given_reg = pickle.load(open("save_given_svm_v5", 'rb'))
  print("Model Saving Complete")

  #test_giving_Collection = db.Give_Fdbck_Accuracy_Model
  print("Creating new users...")

  for i in range(1, 10000):

      chat = random.randrange(1, 6)
      safe = random.randrange(1, 6)
      punctual = random.randrange(1, 6)
      friend = random.randrange(1, 6)
      comfort = random.randrange(1, 6)
      UTT_r = random.randrange(2, 7)
      UTT = UTT_r * 5
      print("ith Users", i ,"New User UTT and Characteristics")
      #print("[UTT, chat, safe, punctual, friend, comfort]")
      print([UTT, chat, safe, punctual, friend, comfort])
      classifier = saved_given_reg.predict([[UTT, chat, safe, punctual, friend, comfort]])
      #print(classifier)
      value_classifier = classifier[0]
      round_classifier = round(value_classifier, 0)
      int_round_classifier = int(round_classifier)
      string_classifier = constants.EMPTY_STRING
      if round_classifier == 1:
          string_classifier = constants.CHATTY_SCORE
      elif round_classifier == 2:
          string_classifier = constants.SAFETY_SCORE
      elif round_classifier == 3:
          string_classifier = constants.PUNCTUALITY_SCORE
      elif round_classifier == 4:
          string_classifier = constants.FRIENDLINESS_SCORE
      elif round_classifier == 5:
          string_classifier = constants.COMFORTIBILITY_SCORE
      test_document = {
          constants.UTT: UTT,
          constants.CHATTY_SCORE: chat,
          constants.SAFETY_SCORE: safe,
          constants.PUNCTUALITY_SCORE: punctual,
          constants.FRIENDLINESS_SCORE: friend,
          constants.COMFORTIBILITY_SCORE: comfort,
          constants.GIVEN_FEEDBACK_CLASSIFIER_INT: int_round_classifier
      }
      print(test_document)
      id = test_giving_Collection.insert_one(test_document)

      print("Give Feedback Classifer is ", round_classifier,  " or ", string_classifier)
      print("---------------------------------------------------")
  #test_giving_Fdback = db.Give_Fdbck_Test
  cursor_test = test_giving_Collection.find()
  df_test = pd.DataFrame(list(cursor_test))
  df_test.to_csv('give_feedback_test_data.csv', index=False)
  df_test = pd.read_csv('give_feedback_test_data.csv')
  score = reg.score(
      df_test[[constants.UTT, constants.CHATTY_SCORE, constants.SAFETY_SCORE, constants.PUNCTUALITY_SCORE,
               constants.FRIENDLINESS_SCORE, constants.COMFORTIBILITY_SCORE]],
      df_test.giving_feedback_classifier_int)
  print("Support Vector Machine Score for Given Feedback Test Data Classifier Score is ", score)
  timestamp = datetime.now().strftime(constants.TIME_STRING)
  svm_test_data_reg = db.testDataGivenScore
  tst_score = {
      constants.TIME_STAMP: timestamp,
      "type": "feedback_predicted_given_test_data",
      constants.SCORE: score
  }
  id_test = svm_test_data_reg.insert_one(tst_score)
  print("Performing F1 Score Test...")
  Give_Fdbck_Test_F1 = db.Give_Fdbck_Test_F1
  Give_Fdbck_Test_F1.drop()
  df_super_test = pd.read_csv('give_feedback_train_data_full.csv')
  print("Read 4000 Computed Records")
  print("Predicting Values Now...")
  for index, row in df_super_test.iterrows():
      chat_super_test = row[constants.CHATTY_SCORE]
      safe_super_test = row[constants.SAFETY_SCORE]
      punctual_super_test = row[constants.PUNCTUALITY_SCORE]
      friend_super_test = row[constants.FRIENDLINESS_SCORE]
      comfort_super_test = row[constants.COMFORTIBILITY_SCORE]
      UTT_super_test = row[constants.UTT]
      classifier_super_test = saved_given_reg.predict([[UTT_super_test, chat_super_test, safe_super_test, punctual_super_test, friend_super_test, comfort_super_test]])
      value_classifier_super_test = classifier_super_test[0]
      round_classifier_super_test = round(value_classifier_super_test, 0)
      int_round_classifier_super_test = int(round_classifier_super_test)
      super_test_document = {
          constants.UTT: UTT_super_test,
          constants.CHATTY_SCORE: chat_super_test,
          constants.SAFETY_SCORE: safe_super_test,
          constants.PUNCTUALITY_SCORE: punctual_super_test,
          constants.FRIENDLINESS_SCORE: friend_super_test,
          constants.COMFORTIBILITY_SCORE: comfort_super_test,
          constants.GIVEN_FEEDBACK_CLASSIFIER_INT: int_round_classifier_super_test
      }
      super_test_given_test_data = db.Give_Fdbck_Test_F1
      id_f1 = super_test_given_test_data.insert_one(super_test_document)
  super_test_given_test_data = db.Give_Fdbck_Test_F1
  cursor_super = super_test_given_test_data.find()
  df_test_csv = pd.DataFrame(list(cursor_super))
  df_test_csv.to_csv('predicted_given_trained_data.csv', index=False)
  f1_score.f1_score_given()
  '''
# supVM_test.supVM_given_test()


'''
    saved_got_reg = pickle.load(open("save_got_svm_v2", 'rb'))
    print("Model Saving Complete")

    for i in range(0, 10000):
        chat = random.randrange(1, 6)
        safe = random.randrange(1, 6)
        punctual = random.randrange(1, 6)
        friend = random.randrange(1, 6)
        comfort = random.randrange(1, 6)
        UTT_r = random.randrange(2, 7)
        UTT = UTT_r * 5
        print("ith Users", i, "New User UTT and Characteristics")
        #print("New User UTT and Characteristics")
        #print("[UTT, chat, safe, punctual, friend, comfort]")
        print([UTT, chat, safe, punctual, friend, comfort])
        classifier = saved_got_reg.predict([[UTT, chat, safe, punctual, friend, comfort]])
        #print(classifier)
        value_classifier = classifier[0]
        round_classifier = round(value_classifier, 0)
        int_round_classifier = int(round_classifier)

        string_classifier = constants.EMPTY_STRING
        if round_classifier == 1:
            string_classifier = constants.CHATTY_SCORE
        elif round_classifier == 2:
            string_classifier = constants.SAFETY_SCORE
        elif round_classifier == 3:
            string_classifier = constants.PUNCTUALITY_SCORE
        elif round_classifier == 4:
            string_classifier = constants.FRIENDLINESS_SCORE
        elif round_classifier == 5:
            string_classifier = constants.COMFORTIBILITY_SCORE

        test_document = {
            constants.UTT: UTT,
            constants.CHATTY_SCORE: chat,
            constants.SAFETY_SCORE: safe,
            constants.PUNCTUALITY_SCORE: punctual,
            constants.FRIENDLINESS_SCORE: friend,
            constants.COMFORTIBILITY_SCORE: comfort,
            constants.GOT_FEEDBACK_CLASSIFIER_INT: int_round_classifier
        }
        test_got_Fdback = db.Got_Fdbck_Test
        test_data_id = test_got_Fdback.insert_one(test_document)

        print("Got Feedback Classifer is ", round_classifier, " or ", string_classifier)
        print("---------------------------------------------------")
    test_got_Fdback = db.Got_Fdbck_Test
    cursor_test = test_got_Fdback.find()
    df_test = pd.DataFrame(list(cursor_test))
    df_test.to_csv('got_feedback_test_data.csv', index=False)
    df_test = pd.read_csv('got_feedback_test_data.csv')
    score = reg.score(df_test[[constants.UTT, constants.CHATTY_SCORE, constants.SAFETY_SCORE, constants.PUNCTUALITY_SCORE,
                             constants.FRIENDLINESS_SCORE, constants.COMFORTIBILITY_SCORE]],
                    df_test.got_feedback_classifier_int)
    print("Support Vector Machine Score for Got Feedback Test Data Classifier Score is ", score)
    timestamp = datetime.now().strftime(constants.TIME_STRING)
    svm_test_data_reg = db.testDataGotScore
    tst_score = {
        constants.TIME_STAMP: timestamp,
        "type": "feedback_predicted_got_test_data",
        constants.SCORE: score
    }
    id_test = svm_test_data_reg.insert_one(tst_score)

    print("Performing F1 Score Test...")
    Got_Fdbck_Test_F1 = db.Got_Fdbck_Test_F1
    Got_Fdbck_Test_F1.drop()
    df_super_test = pd.read_csv('got_feedback_train_data_full.csv')
    print("Read 4000 Computed Records")
    print("Predicting Values Now...")
    for index, row in df_super_test.iterrows():
        chat_super_test = row[constants.CHATTY_SCORE]
        safe_super_test = row[constants.SAFETY_SCORE]
        punctual_super_test = row[constants.PUNCTUALITY_SCORE]
        friend_super_test = row[constants.FRIENDLINESS_SCORE]
        comfort_super_test = row[constants.COMFORTIBILITY_SCORE]
        UTT_super_test = row[constants.UTT]
        classifier_super_test = saved_got_reg.predict([[UTT_super_test, chat_super_test, safe_super_test,
                                                          punctual_super_test, friend_super_test, comfort_super_test]])
        value_classifier_super_test = classifier_super_test[0]
        round_classifier_super_test = round(value_classifier_super_test, 0)
        int_round_classifier_super_test = int(round_classifier_super_test)
        super_test_document = {
            constants.UTT: UTT_super_test,
            constants.CHATTY_SCORE: chat_super_test,
            constants.SAFETY_SCORE: safe_super_test,
            constants.PUNCTUALITY_SCORE: punctual_super_test,
            constants.FRIENDLINESS_SCORE: friend_super_test,
            constants.COMFORTIBILITY_SCORE: comfort_super_test,
            constants.GOT_FEEDBACK_CLASSIFIER_INT: int_round_classifier_super_test
        }
        super_test_got_test_data = db.Got_Fdbck_Test_F1
        id_f1 = super_test_got_test_data.insert_one(super_test_document)
    super_test_got_test_data = db.Got_Fdbck_Test_F1
    cursor_super = super_test_got_test_data.find()
    df_test_csv = pd.DataFrame(list(cursor_super))
    df_test_csv.to_csv('predicted_got_trained_data.csv', index=False)
    f1_score.f1_score_got()
       '''
# supVM_test.supVM_got_test()
"""
This file stores discarted codes that are not in use but may be helpful to look at later
"""

def high_dim_sldsc(args):
    if args.standardize:
        # match snps between annotation ld, sumstats and weights, store new files in output-folder, return new file names
        ld_fname,ss_fname,w_fname = d.match_snps(args)
        # split data into training and test according to user specified left out region
        # return array of indices for training and test sets store them in files
        ld_train,ss_train,w_train,ld_test,ss_test,w_test = d.split_data(ld_fname,ss_fname,w_fname,args)        # compute true weights for training data, true weights are the variance of noise
        true_train_weights = d.compute_weights(ld_train,ss_train,w_train,args)
        # create new target by computing chisq-1, store new target
        ttrain_fname = d.new_target(ss_train,args)
        # standardize training ld and store the standardized ld, mean and standard deviation
        stdized_ldtr_fname,mldtr_fname,sldtr_fname = d.standardize_ld(ld_train,args)
        # standardize training ss-1, store it in a new file, together with mean and standard deviation
        stdized_ttr_fname,mttr_fname,sttr_fname = d.standardize_target(ttrain_fname,args)
        # scale train weights so that it has variance 1
        scaled_train_weights = d.scale_train_weights(true_train_weights)
        if args.single-method:
            # run regression with one method
            # store results to file
            coef_fname,bias_fname = r.run_reg_one_method(stdized_ldtr_fname,stdized_ttr_fname,scaled_train_weights,args)
            # use the learned coefs and bias to predict summary statistics on the test data
            p.predict_one_method(coef_fname,bias_fname,mldtr_fname,sldtr_fname,mttr_fname,sttr_fname,args)
        elif args.multi-methods:
            # run regression with multiple methods
            # store results to file
            coef_fname,bias_fname = r.run_reg_multi_methods(stdized_ldtr_fname,stdized_ttr_fname,scaled_train_weights,args)
            p.predict_multi_methods(coef_fname,bias_fname,mldtr_fname,sldtr_fname,mttr_fname,sttr_fname,args)


# the old process function
def process(args,train_data):
    # compute and store true weights
    true_weights = compute_true_w(args,train_data)
    true_w_df = pd.DataFrame(data=true_weights,columns=['TRUE_W'])
    true_w_fname = args.output_folder+'true_weights.txt'
    true_w_df.to_csv(true_w_fname,sep='\t',index=False)
    # compute and store chisq-1
    ss_df = pd.read_csv(train_data.y,delim_whitespace=True).iloc[train_data.active_ind,:]
    chisq = ss_df['CHISQ'].tolist()
    chisq_minus1 = [x-1 for x in chisq]
    minus1_df = pd.DataFrame(data=chisq_minus1,columns=['CHISQ-1'])
    minus1_fname = args.output_folder+'chisq_minus1.txt'
    minus1_df.to_csv(minus1_fname,sep='\t',index=False)
    return data(args.ld,minus1_fname,true_w_fname,train_data.active_ind)

    weights_scaled = d.scale_weights(weights) #TODO: write this function
    s_weights_df = pd.DataFrame(data=weights_scaled,columns=['SCALED_W'])
    weights_fname = args.output_folder+'scaled_weights.txt'
    s_weights_df.to_csv(weights_fname,sep='\t',index=False)

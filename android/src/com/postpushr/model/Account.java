package com.postpushr.model;

import java.util.List;

public class Account {

	private final String[] mEmailAddresses;
	private final String mHashedSaltedPassword;
	private final String mName;
	private final CreditCard[] mCreditCards;
	private final String mReturnAddress;
	private final List<Order> mOrders;

	public Account(String[] emailAddresses, String hashedSaltedPassword,
			String name, CreditCard[] creditCards, String returnAddress, List<Order> orders) {
		mEmailAddresses = emailAddresses;
		mHashedSaltedPassword = hashedSaltedPassword;
		mName = name;
		mCreditCards = creditCards;
		mReturnAddress = returnAddress;
		mOrders = orders;
	}

	public String getUsername() {
		return mEmailAddresses[0];
	}
	
	public String[] getEmails() {
		return mEmailAddresses;
	}
	
	public String getHashedSaltedPassword() {
		return mHashedSaltedPassword;
	}
	
	public String getName() {
		return mName;
	}
	
	public CreditCard[] getCreditCards() {
		return mCreditCards;
	}
	
	public String getReturnAddress() {
		return mReturnAddress;
	}
	
	public List<Order> getOrders() {
		return mOrders;
	}
}

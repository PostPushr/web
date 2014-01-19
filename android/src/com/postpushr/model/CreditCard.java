package com.postpushr.model;

public class CreditCard {

	private final String mCardNumber;
	private final int mExpirationMonth;
	private final int mExpirationYear;
	private final int mSecurityCode;
	private final String mStripeToken;
	
	public CreditCard(String cardNumber, int expirationMonth, int expirationYear, int securityCode, String stripeToken) {
		mCardNumber = cardNumber;
		mExpirationMonth = expirationMonth;
		mExpirationYear = expirationYear;
		mSecurityCode = securityCode;
		mStripeToken = stripeToken;
	}
	
	public String getCardNumber() {
		return mCardNumber;
	}
	
	public int getExpirationMonth() {
		return mExpirationMonth;
	}
	
	public int getExpirationYear() {
		return mExpirationYear;
	}
	
	public int getSecurityCode() {
		return mSecurityCode;
	}
	
	public String getStripeToken() {
		return mStripeToken;
	}
	
}

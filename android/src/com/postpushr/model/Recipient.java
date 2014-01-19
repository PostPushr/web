package com.postpushr.model;

public class Recipient {

	private final String mName;
	private final String mAddress;
	
	public Recipient(String name, String address) {
		mName = name;
		mAddress = address;
	}
	
	public String getName() {
		return mName;
	}
	
	public String getAddress() {
		return mAddress;
	}
}

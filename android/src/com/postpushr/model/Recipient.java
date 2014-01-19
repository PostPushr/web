package com.postpushr.model;

public class Recipient {

	private final String mName;
	private final String mAddress;
	private final String mMessage;

	public Recipient(String name, String address, String message) {
		mName = name;
		mAddress = address;
		mMessage = message;
	}

	public String getName() {
		return mName;
	}

	public String getAddress() {
		return mAddress;
	}

	public String getMessage() {
		return mMessage;
	}
}

package com.postpushr.model;

import java.util.List;

public class Account {

	private final String mUsername;
	private final String mHashedSaltedPassword;
	private final List<Order> mOrders;

	public Account(String username, String hashedSaltedPassword,
			List<Order> orders) {
		mUsername = username;
		mHashedSaltedPassword = hashedSaltedPassword;
		mOrders = orders;
	}

	public String getUsername() {
		return mUsername;
	}

	public String getHashedSaltedPassword() {
		return mHashedSaltedPassword;
	}

	public List<Order> getOrders() {
		return mOrders;
	}
}

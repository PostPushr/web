package com.postpushr.model;

import android.annotation.SuppressLint;
import android.graphics.Bitmap;

public class Order {

	private final String mOrderDate;
	private final Bitmap mPicture;
	private final Recipient mRecipient;
	private final float mPrice;

	public Order(String orderDate, Bitmap picture, Recipient recipient, float price) {
		mOrderDate = orderDate;
		mPicture = picture;
		mRecipient = recipient;
		mPrice = price;
	}

	public String getOrderDateString() {
		// TODO test this formatting
		return mOrderDate;
	}

	public Bitmap getPicture() {
		return mPicture;
	}

	public Recipient getRecipient() {
		return mRecipient;
	}

	@SuppressLint("DefaultLocale")
	public String getPriceString() {
		// TODO test this formatting
		return String.format("%.2f", mPrice);
	}

}

package com.postpushr.fragments;

import android.app.ListFragment;
import android.content.Context;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.TextView;

import com.postpushr.R;
import com.postpushr.model.Account;
import com.postpushr.model.Order;

public class HomeFragment extends ListFragment {

	private Account mAccount;

	@Override
	public void onCreate(Bundle savedInstanceState) {

	}

	private class OrderListAdapter extends BaseAdapter {

		private final Context mContext;

		public OrderListAdapter(Context context) {
			mContext = context;
		}

		@Override
		public int getCount() {
			return mAccount.getOrders().size();
		}

		@Override
		public Object getItem(int position) {
			return mAccount.getOrders().get(position);
		}

		@Override
		public long getItemId(int position) {
			return position;
		}

		// TODO: Add thumbnails to each order row
		@Override
		public View getView(int position, View view, ViewGroup parent) {

			if (null == view) {
				LayoutInflater layoutInflater = (LayoutInflater) mContext
						.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
				view = layoutInflater.inflate(R.layout.order_row, parent);
			}

			TextView orderName = (TextView) view
					.findViewById(R.id.order_row_date_textview);
			orderName.setText(((Order) getItem(position)).getOrderDateString());

			return null;
		}
	}
}

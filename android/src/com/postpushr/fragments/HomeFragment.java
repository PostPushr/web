package com.postpushr.fragments;

import android.app.ListFragment;
import android.content.Context;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.TextView;

import com.postpushr.R;
import com.postpushr.model.Account;
import com.postpushr.model.Order;

public class HomeFragment extends ListFragment {

	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setHasOptionsMenu(true);
	}

	@Override
	public void onCreateOptionsMenu(Menu menu, MenuInflater inflater) {
		inflater.inflate(R.menu.home_actionbar, menu);
	}

	@Override
	public boolean onOptionsItemSelected(MenuItem item) {
		switch (item.getItemId()) {
		case (R.id.home_actionbar_add_button):
			((PostcardFlowListener) getActivity()).switchToAddPostcardFragment();
			return true;
		default:
			return super.onOptionsItemSelected(item);
		}
	}

	public class OrderListAdapter extends BaseAdapter {

		private final Context mContext;
		private final Account mAccount;

		public OrderListAdapter(Context context, Account account) {
			mContext = context;
			mAccount = account;
		}

		@Override
		public int getCount() {
			if (mAccount.getOrders() != null) {
				return mAccount.getOrders().size();
			} else {
				return 0;
			}
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
				LayoutInflater layoutInflater = (LayoutInflater) mContext.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
				view = layoutInflater.inflate(R.layout.order_row, parent);
			}

			TextView orderName = (TextView) view.findViewById(R.id.order_row_date_textview);
			orderName.setText(((Order) getItem(position)).getOrderDateString());

			return null;
		}
	}

	public interface PostcardFlowListener {
		public void switchToAddPostcardFragment();

		public void executePostcardCameraIntent();

		public int getPostcardCode();

		public int getSelfieCode();

	}
}

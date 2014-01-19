package com.postpushr.fragments;

import java.util.ArrayList;
import java.util.List;

import android.app.Fragment;
import android.content.Context;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.View.OnClickListener;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.Button;
import android.widget.ListAdapter;
import android.widget.ListView;

import com.postpushr.R;
import com.postpushr.model.Recipient;

public class AddPostcardFragment extends Fragment {

	private List<Recipient> mRecipients;
	private ListAdapter mAdapter;

	@Override
	public void onCreate(Bundle savedInstanceState) {
		mRecipients = new ArrayList<Recipient>();
		mRecipients.add(new Recipient(null, null, null));
		super.onCreate(savedInstanceState);
		setHasOptionsMenu(true);
	}

	/*
	 * @Override public void onCreateOptionsMenu(Menu menu, MenuInflater
	 * inflater) {
	 * menu.findItem(R.id.home_actionbar_add_button).setVisible(false); }
	 */

	@Override
	public View onCreateView(LayoutInflater inflater, ViewGroup parent, Bundle savedInstanceState) {
		View view = inflater.inflate(R.layout.fragment_addpostcard, parent, false);

		Button takePictureButton = (Button) view.findViewById(R.id.addpostcard_takepicture_button);
		takePictureButton.setOnClickListener(new TakePictureListener());

		ListView recipientsListView = (ListView) view.findViewById(R.id.addpostcard_recipients_listview);
		mAdapter = new RecipientsListAdapter();
		recipientsListView.setAdapter(mAdapter);

		Button addRecipientButton = (Button) view.findViewById(R.id.addpostcard_addrecipient_button);
		addRecipientButton.setOnClickListener(new AddRecipientListener());

		Button sendPostcardButton = (Button) view.findViewById(R.id.addpostcard_send_button);
		sendPostcardButton.setOnClickListener(new PostcardSendListener());

		return view;
	}

	private class TakePictureListener implements OnClickListener {

		@Override
		public void onClick(View arg0) {
			// TODO Auto-generated method stub

		}

	}

	private class RecipientsListAdapter extends BaseAdapter {

		@Override
		public int getCount() {
			return mRecipients.size();
		}

		@Override
		public Object getItem(int position) {
			return mRecipients.get(position);
		}

		@Override
		public long getItemId(int position) {
			return position;
		}

		@Override
		public View getView(int position, View view, ViewGroup parent) {
			if (null == view) {
				LayoutInflater inflater = (LayoutInflater) getActivity().getSystemService(Context.LAYOUT_INFLATER_SERVICE);
				view = inflater.inflate(R.layout.recipient_row, null);
			}
			return view;
		}

	}

	private class AddRecipientListener implements OnClickListener {

		@Override
		public void onClick(View arg0) {
			mRecipients.add(new Recipient(null, null, null));
			((BaseAdapter) mAdapter).notifyDataSetChanged();
		}

	}

	private class PostcardSendListener implements OnClickListener {
		@Override
		public void onClick(final View view) {

		}
	}
}